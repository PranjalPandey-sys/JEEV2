"""
services/media.py
Bulletproof image sending: file_id → local file → text-only fallback.
Never crashes the bot.
"""
import logging
import os
from telegram import InlineKeyboardMarkup, Message
from telegram.constants import ParseMode
from telegram.error import BadRequest, TelegramError

import config

logger = logging.getLogger(__name__)


async def send_photo(
    message,                   # telegram.Message object
    key: str,                  # key in config.IMAGES / config.IMG_LOCAL
    caption: str,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> Message | None:
    """
    Send a photo with caption.
    Priority: cached file_id  →  local file  →  text-only.
    Caches file_id on first successful upload.
    Always returns safely; never raises.
    """

    # ── 1. Try cached file_id ─────────────────────────────────────────────────
    file_id = config.IMAGES.get(key, "")
    if file_id:
        try:
            msg = await message.reply_photo(
                photo=file_id,
                caption=caption,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
            )
            return msg
        except (BadRequest, TelegramError) as e:
            # file_id stale or invalid — clear it and fall through
            logger.warning(f"[media] Stale file_id for '{key}': {e}. Clearing.")
            config.IMAGES[key] = ""

    # ── 2. Try local file ─────────────────────────────────────────────────────
    local_path = config.IMG_LOCAL.get(key, "")
    if local_path and os.path.exists(local_path):
        try:
            with open(local_path, "rb") as f:
                msg = await message.reply_photo(
                    photo=f,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                )
            # Cache the returned file_id for future sends
            if msg and msg.photo:
                config.IMAGES[key] = msg.photo[-1].file_id
                logger.info(f"[media] Cached file_id for '{key}': {config.IMAGES[key]}")
            return msg
        except TelegramError as e:
            logger.warning(f"[media] Local file send failed for '{key}': {e}")

    # ── 3. Text-only fallback ─────────────────────────────────────────────────
    try:
        msg = await message.reply_text(
            caption,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
        )
        return msg
    except TelegramError as e:
        logger.error(f"[media] Even text fallback failed for '{key}': {e}")
        return None
