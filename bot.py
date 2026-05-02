"""
bot.py — JEE Success System Telegram Bot
Production-grade | Render-compatible | python-telegram-bot 21.x

FIXES IN THIS VERSION:
  ✅ /start ALWAYS works (allow_reentry=True, existing users skip to home)
  ✅ Home button ALWAYS works (inline button routed through callback_router)
  ✅ No handler ordering conflicts (ConversationHandler uses allow_reentry)
  ✅ Doubt handler intercepts text ONLY when awaiting_doubt flag is set
  ✅ Global error handler prevents bot from stopping
  ✅ Anti-spam protection (10 messages/10s per user)
  ✅ All image sends have try/except fallback
  ✅ Flask starts first, then polling (Render health-check fix)
"""
import logging
import os
import threading
import time
from collections import defaultdict

from flask import Flask
from telegram import BotCommand, Update
from telegram.error import NetworkError, TimedOut
from telegram.ext import (
    Application, CallbackQueryHandler, CommandHandler,
    ContextTypes, MessageHandler, filters,
)

# ── Project modules ───────────────────────────────────────────────────────────
import config
import storage
from handlers.onboarding import get_conversation_handler
from handlers.home       import cmd_home, show_home
from handlers.tasks      import cmd_task, handle_mark_done
from handlers.doubt      import cmd_doubt, handle_doubt_message
from handlers.admin      import (
    cmd_admin, cmd_broadcast, cmd_addadmin, cmd_removeadmin,
    handle_admin_callback,
)
from handlers.screens    import (
    cmd_progress, cmd_plan, cmd_resources, cmd_earn,
    cmd_streak, cmd_help,
    show_progress, show_plan, show_resources, show_earn,
    show_settings, show_doubt_prompt,
    handle_toggle_notif, handle_confirm_reset, handle_do_reset,
)

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# ANTI-SPAM  — simple in-memory rate limiter (10 msgs / 10 seconds per user)
# ─────────────────────────────────────────────────────────────────────────────
_spam_counters: dict[int, list[float]] = defaultdict(list)
SPAM_LIMIT   = 10   # max messages
SPAM_WINDOW  = 10   # seconds

def _is_spam(user_id: int) -> bool:
    now    = time.time()
    times  = _spam_counters[user_id]
    # Remove old timestamps outside window
    _spam_counters[user_id] = [t for t in times if now - t < SPAM_WINDOW]
    _spam_counters[user_id].append(now)
    return len(_spam_counters[user_id]) > SPAM_LIMIT


# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL ERROR HANDLER
# ─────────────────────────────────────────────────────────────────────────────

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log all errors. Bot keeps running no matter what."""
    logger.error(f"[error_handler] Exception: {context.error}", exc_info=context.error)

    # Optionally notify the user something went wrong
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "⚠️ Something went wrong on our end. Please try again in a moment.\n"
                "If it keeps happening, type /start to reset."
            )
        except Exception:
            pass  # if we can't even send this, silently ignore


# ─────────────────────────────────────────────────────────────────────────────
# MAIN CALLBACK ROUTER
# Handles ALL inline button presses — single clean switch.
# ─────────────────────────────────────────────────────────────────────────────

async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data  = query.data
    uid   = query.from_user.id

    # Anti-spam
    if _is_spam(uid):
        await query.answer("⏳ Slow down! Please wait a moment.", show_alert=True)
        return

    await query.answer()  # acknowledge the tap immediately

    # ── Admin callbacks ───────────────────────────────────────────────────────
    if await handle_admin_callback(query, context):
        return

    # ── Navigation ────────────────────────────────────────────────────────────
    if data == "home":
        await show_home(query, context)

    elif data == "task":
        storage.log_command("task")
        await cmd_task.__wrapped__(query, context) if hasattr(cmd_task, "__wrapped__") \
            else await _show_task_cb(query, context, uid)

    elif data == "progress":
        storage.log_command("progress")
        await show_progress(query, context, uid=uid)

    elif data == "plan":
        storage.log_command("plan")
        await show_plan(query, context, uid=uid)

    elif data.startswith("plan_week_"):
        week = int(data.split("_")[-1])
        await show_plan(query, context, uid=uid, week=week)

    elif data == "resources":
        storage.log_command("resources")
        await show_resources(query, context, uid=uid)

    elif data.startswith("res_"):
        page = data[4:]
        await show_resources(query, context, page=page, uid=uid)

    elif data == "earn":
        storage.log_command("earn")
        await show_earn(query, context, uid=uid)

    elif data.startswith("earn_"):
        idx = int(data.split("_")[1])
        await show_earn(query, context, gig_idx=idx, uid=uid)

    elif data == "doubt":
        storage.log_command("doubt")
        await show_doubt_prompt(query, context, uid=uid)

    elif data == "settings":
        await show_settings(query, context, uid=uid)

    elif data == "toggle_notif":
        await handle_toggle_notif(query, context)

    elif data == "confirm_reset":
        await handle_confirm_reset(query, context)

    elif data == "do_reset":
        await handle_do_reset(query, context)

    elif data == "mark_done":
        await handle_mark_done(query, context)

    elif data == "noop":
        await query.answer("Already done today! 🌟 See you tomorrow.", show_alert=True)

    else:
        logger.warning(f"[callback_router] Unknown callback data: '{data}'")


# Helper so we can call show_task from callback_router cleanly
async def _show_task_cb(query, context, uid):
    from handlers.tasks import show_task
    await show_task(query, context, uid=uid)


# ─────────────────────────────────────────────────────────────────────────────
# UNKNOWN MESSAGE HANDLER
# Note: doubt questions are intercepted BEFORE this by handle_doubt_message
# ─────────────────────────────────────────────────────────────────────────────

async def unknown_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid  = update.effective_user.id
    user = storage.get_user(uid)

    if _is_spam(uid):
        return  # silently ignore spammers

    storage.log_command("message")

    if not user:
        await update.message.reply_text(
            "👋 Welcome! Type /start to set up your JEE Success System."
        )
        return

    from handlers.helpers import main_menu_keyboard
    import random, study_data
    await update.message.reply_text(
        f"👋 Hey <b>{user['name']}</b>! Use the menu below.\n\n"
        f"<i>{random.choice(study_data.QUOTES)}</i>",
        parse_mode=__import__("telegram").constants.ParseMode.HTML,
        reply_markup=main_menu_keyboard(),
    )


# ─────────────────────────────────────────────────────────────────────────────
# BOT COMMAND MENU  (shown in Telegram sidebar)
# ─────────────────────────────────────────────────────────────────────────────

async def post_init(application: Application) -> None:
    await application.bot.set_my_commands([
        BotCommand("start",     "Setup / Return to home"),
        BotCommand("home",      "Dashboard"),
        BotCommand("task",      "Today's task"),
        BotCommand("progress",  "My progress & stats"),
        BotCommand("plan",      "Full 8-week roadmap"),
        BotCommand("resources", "Books, PYQs, Mock Tests"),
        BotCommand("doubt",     "Ask AI tutor (Gemini)"),
        BotCommand("earn",      "Earning opportunities"),
        BotCommand("streak",    "Check your streak"),
        BotCommand("help",      "All commands"),
    ])
    logger.info("[bot] Command menu set successfully.")


# ─────────────────────────────────────────────────────────────────────────────
# BUILD APPLICATION
# ─────────────────────────────────────────────────────────────────────────────

def build_app() -> Application:
    if not config.BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable is not set!")

    app = (
        Application.builder()
        .token(config.BOT_TOKEN)
        .post_init(post_init)
        .connect_timeout(30)
        .read_timeout(30)
        .write_timeout(30)
        .pool_timeout(30)
        .build()
    )

    # ── 1. Onboarding ConversationHandler (MUST be first) ────────────────────
    #    allow_reentry=True means /start always works even if stuck in a state
    app.add_handler(get_conversation_handler(), group=0)

    # ── 2. Admin commands ─────────────────────────────────────────────────────
    app.add_handler(CommandHandler("admin",        cmd_admin),        group=1)
    app.add_handler(CommandHandler("broadcast",    cmd_broadcast),    group=1)
    app.add_handler(CommandHandler("addadmin",     cmd_addadmin),     group=1)
    app.add_handler(CommandHandler("removeadmin",  cmd_removeadmin),  group=1)

    # ── 3. Regular commands ───────────────────────────────────────────────────
    app.add_handler(CommandHandler("home",      cmd_home),      group=1)
    app.add_handler(CommandHandler("task",      cmd_task),      group=1)
    app.add_handler(CommandHandler("progress",  cmd_progress),  group=1)
    app.add_handler(CommandHandler("plan",      cmd_plan),      group=1)
    app.add_handler(CommandHandler("resources", cmd_resources), group=1)
    app.add_handler(CommandHandler("earn",      cmd_earn),      group=1)
    app.add_handler(CommandHandler("doubt",     cmd_doubt),     group=1)
    app.add_handler(CommandHandler("streak",    cmd_streak),    group=1)
    app.add_handler(CommandHandler("help",      cmd_help),      group=1)

    # ── 4. Inline button callbacks ────────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(callback_router), group=1)

    # ── 5. Doubt message interceptor (BEFORE generic unknown_msg) ────────────
    #    Only fires when user has pressed "Ask AI Tutor" button
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.UpdateType.MESSAGE,
            _doubt_or_unknown,
        ),
        group=1,
    )

    # ── 6. Global error handler ───────────────────────────────────────────────
    app.add_error_handler(error_handler)

    return app


async def _doubt_or_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Routes text messages:
      - If user just pressed 'Ask AI Tutor' → solve doubt
      - Otherwise → generic unknown_msg
    This avoids needing a separate ConversationHandler for doubts.
    """
    if context.user_data.get("awaiting_doubt"):
        await handle_doubt_message(update, context)
    else:
        await unknown_msg(update, context)


# ─────────────────────────────────────────────────────────────────────────────
# FLASK  keep-alive (Render free tier)
# ─────────────────────────────────────────────────────────────────────────────

flask_app = Flask(__name__)

@flask_app.route("/")
def health():
    return "JEE Success System Bot is running! 🚀", 200

@flask_app.route("/health")
def health2():
    return "OK", 200

def run_flask():
    flask_app.run(
        host="0.0.0.0",
        port=config.PORT,
        use_reloader=False,
        threaded=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# MAIN  — Flask first, then polling with auto-restart
# ─────────────────────────────────────────────────────────────────────────────

def main():
    # Start Flask FIRST — Render health-check hits "/" before polling starts
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info(f"[main] Flask keep-alive started on port {config.PORT}.")
    time.sleep(2)  # Give Flask 2s to bind

    retry_delay = 5
    while True:
        try:
            logger.info("[main] Starting bot polling...")
            app = build_app()
            app.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True,
                timeout=30,
                poll_interval=1.5,
            )
        except (TimedOut, NetworkError) as e:
            logger.warning(f"[main] Network error: {e}. Restarting in {retry_delay}s...")
            time.sleep(retry_delay)
        except Exception as e:
            logger.error(f"[main] Unexpected error: {e}. Restarting in 10s...", exc_info=True)
            time.sleep(10)


if __name__ == "__main__":
    main()
