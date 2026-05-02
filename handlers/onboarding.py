"""
handlers/onboarding.py
/start command and new-user onboarding conversation.

FIX: ConversationHandler only activates for NEW users.
     Existing users skip straight to home — so /start always works.
"""
import logging
from datetime import date

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler, CommandHandler, ContextTypes,
    ConversationHandler, MessageHandler, filters,
)

import storage
from handlers.helpers import send_screen, main_menu_keyboard

logger = logging.getLogger(__name__)

# Conversation states
ASK_NAME, ASK_YEAR = range(2)


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY: /start
# ─────────────────────────────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    uid      = update.effective_user.id
    existing = storage.get_user(uid)

    # Already set up → show home immediately, end conversation
    if existing and existing.get("setup_complete"):
        from handlers.home import show_home
        await show_home(update, context)
        return ConversationHandler.END

    # New user → welcome screen
    caption = (
        "🎓 <b>Welcome to JEE Success System!</b>\n\n"
        "<i>Plan. Execute. Succeed.</i>\n\n"
        "Your daily guide to crack JEE and build a better future.\n\n"
        "Let's set up your personalised roadmap in <b>30 seconds</b>.\n\n"
        "👇 <b>What's your name?</b>"
    )
    await send_screen(update, context, "welcome", caption)
    return ASK_NAME


# ─────────────────────────────────────────────────────────────────────────────
# STATE 1: collect name
# ─────────────────────────────────────────────────────────────────────────────

async def onboard_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    name = update.message.text.strip()

    if not name or len(name) > 30:
        await update.message.reply_text(
            "⚠️ Please enter a valid name (max 30 characters)."
        )
        return ASK_NAME

    context.user_data["onboard_name"] = name

    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("JEE 2025", callback_data="year_2025"),
        InlineKeyboardButton("JEE 2026", callback_data="year_2026"),
        InlineKeyboardButton("JEE 2027", callback_data="year_2027"),
    ]])
    await update.message.reply_text(
        f"Great, <b>{name}</b>! 🙌\n\nWhich year are you targeting?",
        parse_mode=ParseMode.HTML,
        reply_markup=kb,
    )
    return ASK_YEAR


# ─────────────────────────────────────────────────────────────────────────────
# STATE 2: collect target year (via inline button)
# ─────────────────────────────────────────────────────────────────────────────

async def onboard_year(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    year     = int(query.data.split("_")[1])
    name     = context.user_data.get("onboard_name", "Aspirant")
    uid      = query.from_user.id
    days_left = (date(year, 4, 1) - date.today()).days

    storage.create_user(uid, name, year)
    storage.update_user(uid, setup_complete=True)

    await query.message.reply_text(
        f"✅ <b>Setup Complete!</b>\n\n"
        f"👤 Name: <b>{name}</b>\n"
        f"🎯 Target: <b>JEE {year}</b>\n"
        f"⏳ Days left: <b>{days_left} days</b>\n\n"
        f"🌱 <b>Beginner Mode activated.</b>\n"
        f"Starting with just <b>1 hour/day</b> — we'll build up gradually.\n\n"
        f"<i>Consistency today, IIT tomorrow. Let's begin! 🚀</i>",
        parse_mode=ParseMode.HTML,
    )

    # Show home dashboard
    from handlers.home import show_home
    await show_home(query, context)
    return ConversationHandler.END


# ─────────────────────────────────────────────────────────────────────────────
# CONVERSATION HANDLER — exported and registered in bot.py
# ─────────────────────────────────────────────────────────────────────────────

def get_conversation_handler() -> ConversationHandler:
    return ConversationHandler(
        # /start triggers this ONLY if user isn't set up
        entry_points=[CommandHandler("start", cmd_start)],
        states={
            ASK_NAME: [
                # Accept any text that isn't a command
                MessageHandler(filters.TEXT & ~filters.COMMAND, onboard_name),
            ],
            ASK_YEAR: [
                CallbackQueryHandler(onboard_year, pattern=r"^year_\d{4}$"),
            ],
        },
        fallbacks=[
            # /start always resets conversation if user types it mid-flow
            CommandHandler("start", cmd_start),
        ],
        # IMPORTANT: allow_reentry=True so /start always works even if state is stuck
        allow_reentry=True,
        per_user=True,
        per_chat=True,
        # name helps with debugging
        name="onboarding",
    )
