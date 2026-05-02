"""
handlers/doubt.py
AI Tutor — handles incoming text questions after user taps "Ask AI Tutor".
"""
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import storage
import config
from services.gemini import solve_doubt

logger = logging.getLogger(__name__)


async def cmd_doubt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Entry via /doubt command."""
    storage.log_command("doubt")
    from handlers.screens import show_doubt_prompt
    await show_doubt_prompt(update, context, uid=update.effective_user.id)


async def handle_doubt_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Intercepts user text messages when awaiting_doubt flag is set.
    Called BEFORE the generic unknown_msg handler.
    """
    uid      = update.effective_user.id
    question = update.message.text.strip()

    # Rate limiting check
    allowed, wait_secs = storage.can_ask_doubt(uid, config.DOUBT_COOLDOWN_SECONDS)
    if not allowed:
        await update.message.reply_text(
            f"⏱ Please wait <b>{wait_secs} seconds</b> before asking another question.",
            parse_mode=ParseMode.HTML,
        )
        return

    # Clear the waiting flag
    context.user_data["awaiting_doubt"] = False

    # Show "typing..." indicator
    await update.message.reply_text(
        "🤖 <b>AI Tutor is solving your doubt...</b>\n\n"
        "<i>This usually takes 5–10 seconds.</i>",
        parse_mode=ParseMode.HTML,
    )

    # Record the ask time for rate limiting
    storage.record_doubt_asked(uid)

    # Call Gemini
    answer = await solve_doubt(question)

    await update.message.reply_text(
        answer,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🤖 Ask Another",  callback_data="doubt")],
            [InlineKeyboardButton("🏠 Back to Home", callback_data="home")],
        ]),
    )
