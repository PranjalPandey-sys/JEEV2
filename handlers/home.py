"""
handlers/home.py
Home dashboard — called from /start, /home command, and "Home" inline button.

FIX: show_home() accepts Update, CallbackQuery, or bare Message uniformly.
     No more "fake_update" hacks.
"""
import logging
from datetime import date

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import storage
from handlers.helpers import phase_emoji, send_screen, main_menu_keyboard

logger = logging.getLogger(__name__)


async def show_home(source, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Show the main dashboard.
    source can be: Update, CallbackQuery, or telegram.Message
    """
    # ── Resolve user_id and message object ───────────────────────────────────
    if hasattr(source, "effective_user"):
        uid = source.effective_user.id        # Update
    elif hasattr(source, "from_user"):
        uid = source.from_user.id             # CallbackQuery
    else:
        uid = source.chat.id                  # Message (fallback)

    user = storage.get_user(uid)
    if not user:
        # User not set up — redirect to /start
        if hasattr(source, "message") and source.message:
            await source.message.reply_text("Please type /start to set up your account.")
        elif hasattr(source, "reply_text"):
            await source.reply_text("Please type /start to set up your account.")
        return

    storage.handle_missed_day(uid)
    stats    = storage.get_stats(uid)
    streak   = stats.get("streak", 0)
    day      = stats.get("current_day", 1)
    phase    = stats.get("phase", "beginner")
    goal     = stats.get("daily_goal_hours", 1.0)
    days_left = stats.get("days_left", 365)

    fire_str = "🔥" * min(streak, 5) if streak > 0 else "❄️ Start your streak!"

    caption = (
        f"👋 <b>Hey {user['name']}!</b>  {phase_emoji(phase)}\n\n"
        f"🗓 <b>Day {day}</b> of your JEE journey\n"
        f"⏳ <b>{days_left} days</b> to JEE {user.get('target_year', 2026)}\n"
        f"🔥 Streak: <b>{streak} day{'s' if streak != 1 else ''}</b>  {fire_str}\n"
        f"⏱ Today's Goal: <b>{goal} hr{'s' if goal != 1 else ''}</b>\n\n"
        f"📌 Phase: <b>{phase.capitalize()}</b>  {phase_emoji(phase)}\n\n"
        f"<i>Discipline today, Dreams tomorrow. Let's execute! 🚀</i>"
    )

    await send_screen(source, context, "home", caption, main_menu_keyboard())


async def cmd_home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /home command."""
    storage.log_command("home")
    await show_home(update, context)
