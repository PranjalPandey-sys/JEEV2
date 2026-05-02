"""
handlers/helpers.py
Shared UI helpers: keyboards, formatters, and the central send_screen()
that every handler calls instead of duplicating send logic.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from services.media import send_photo


# ─────────────────────────────────────────────────────────────────────────────
# KEYBOARDS
# ─────────────────────────────────────────────────────────────────────────────

def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📅 Today's Task",    callback_data="task"),
            InlineKeyboardButton("📊 My Progress",     callback_data="progress"),
        ],
        [
            InlineKeyboardButton("🗺️ Full Plan",       callback_data="plan"),
            InlineKeyboardButton("📚 Study Resources", callback_data="resources"),
        ],
        [
            InlineKeyboardButton("🤖 Ask AI Tutor",    callback_data="doubt"),
            InlineKeyboardButton("💰 Earn",            callback_data="earn"),
        ],
        [
            InlineKeyboardButton("⚙️ Settings",        callback_data="settings"),
        ],
    ])

def back_home_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Back to Home", callback_data="home")]
    ])

def back_keyboard(back_to: str = "home", label: str = "🏠 Back to Home") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(label, callback_data=back_to)]
    ])


# ─────────────────────────────────────────────────────────────────────────────
# PHASE helpers
# ─────────────────────────────────────────────────────────────────────────────

def phase_emoji(phase: str) -> str:
    return {"beginner": "🌱", "intermediate": "🔥", "advanced": "⚡"}.get(phase, "🌱")


# ─────────────────────────────────────────────────────────────────────────────
# PROGRESS BAR
# ─────────────────────────────────────────────────────────────────────────────

def progress_bar(pct: float, width: int = 10) -> str:
    filled = int(min(pct, 100) / 100 * width)
    return "█" * filled + "░" * (width - filled)


# ─────────────────────────────────────────────────────────────────────────────
# CENTRAL send_screen
# Works for both Update objects and CallbackQuery objects.
# ─────────────────────────────────────────────────────────────────────────────

async def send_screen(
    source,   # Update or CallbackQuery
    context: ContextTypes.DEFAULT_TYPE,
    image_key: str,
    caption: str,
    keyboard: InlineKeyboardMarkup | None = None,
) -> None:
    """
    Unified sender that handles Update, CallbackQuery, and bare Message objects.
    Always sends a new message (no editing) to keep nav simple and stable.
    """
    # Resolve to a telegram.Message object
    if hasattr(source, "message") and source.message:
        msg = source.message          # Update or CallbackQuery
    elif hasattr(source, "effective_message") and source.effective_message:
        msg = source.effective_message
    else:
        msg = source                   # already a Message

    await send_photo(msg, image_key, caption, keyboard)
