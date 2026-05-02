"""
handlers/admin.py
Admin panel — secured by user ID check.
Admins: @radheshyam001, @IamPranjal09

Commands:
  /admin        — Admin menu
  /broadcast    — Send message to all users
  /userstats    — Total users + activity
  /addadmin     — Add a new admin by user ID
  /removeadmin  — Remove an admin by user ID
"""
import asyncio
import logging
import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import config
import storage

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# SECURITY: is_admin check
# ─────────────────────────────────────────────────────────────────────────────

def is_admin(user) -> bool:
    """
    Check if a Telegram user is an admin.
    Checks both numeric ID (config.ADMIN_IDS) and username (config.ADMIN_USERNAMES).
    """
    if user.id in config.ADMIN_IDS:
        return True
    if user.username and user.username.lower() in {u.lower() for u in config.ADMIN_USERNAMES}:
        return True
    return False


async def require_admin(update: Update) -> bool:
    """Returns True if admin, else sends denial message and returns False."""
    if is_admin(update.effective_user):
        return True
    await update.message.reply_text(
        "⛔ <b>Access Denied</b>\n\nThis command is for admins only.",
        parse_mode=ParseMode.HTML,
    )
    logger.warning(
        f"[admin] Unauthorised access attempt by {update.effective_user.id} "
        f"(@{update.effective_user.username})"
    )
    return False


# ─────────────────────────────────────────────────────────────────────────────
# /admin  — main admin menu
# ─────────────────────────────────────────────────────────────────────────────

async def cmd_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await require_admin(update):
        return

    users    = storage.list_all_users()
    total    = len(users)
    active   = sum(1 for u in users if u.get("streak", 0) > 0)
    analytics = storage.get_analytics()
    total_msgs = analytics.get("total_messages", 0)

    # Top commands
    cmds = analytics.get("commands", {})
    top_cmds = sorted(cmds.items(), key=lambda x: x[1], reverse=True)[:5]
    cmd_lines = "\n".join(f"  /{k}: {v}" for k, v in top_cmds) or "  No data yet"

    text = (
        f"👑 <b>ADMIN PANEL</b>\n\n"
        f"👥 Total users: <b>{total}</b>\n"
        f"🔥 Users with active streak: <b>{active}</b>\n"
        f"📨 Total messages handled: <b>{total_msgs}</b>\n\n"
        f"📊 <b>Top Commands</b>\n{cmd_lines}\n\n"
        f"<i>Use the buttons below to manage the bot.</i>"
    )

    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📢 Broadcast",   callback_data="admin_broadcast"),
            InlineKeyboardButton("📊 User Stats",  callback_data="admin_stats"),
        ],
        [
            InlineKeyboardButton("👥 List Users",  callback_data="admin_users"),
            InlineKeyboardButton("📈 Analytics",   callback_data="admin_analytics"),
        ],
    ])
    await update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=kb)


# ─────────────────────────────────────────────────────────────────────────────
# /broadcast  — send message to all users
# ─────────────────────────────────────────────────────────────────────────────

async def cmd_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await require_admin(update):
        return

    # Message to broadcast is everything after /broadcast
    args = context.args
    if not args:
        await update.message.reply_text(
            "📢 <b>Broadcast Usage:</b>\n\n"
            "<code>/broadcast Your message here</code>\n\n"
            "This will send your message to ALL users.",
            parse_mode=ParseMode.HTML,
        )
        return

    message_text = " ".join(args)
    user_ids     = storage.get_all_user_ids()
    total        = len(user_ids)

    if total == 0:
        await update.message.reply_text("No users to broadcast to.")
        return

    # Confirm before sending
    context.user_data["broadcast_text"] = message_text
    await update.message.reply_text(
        f"📢 <b>Broadcast Preview</b>\n\n"
        f"<i>{message_text}</i>\n\n"
        f"This will be sent to <b>{total} users</b>.\n"
        f"Confirm?",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ Send",    callback_data="admin_broadcast_confirm"),
            InlineKeyboardButton("❌ Cancel",  callback_data="admin_broadcast_cancel"),
        ]]),
    )


async def execute_broadcast(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Actually sends the broadcast after confirmation."""
    message_text = context.user_data.get("broadcast_text", "")
    if not message_text:
        await query.message.reply_text("No broadcast message set.")
        return

    user_ids  = storage.get_all_user_ids()
    sent      = 0
    failed    = 0
    start     = time.time()

    status_msg = await query.message.reply_text(
        f"📢 Broadcasting to {len(user_ids)} users... Please wait."
    )

    for uid in user_ids:
        try:
            await context.bot.send_message(
                chat_id=uid,
                text=(
                    f"📢 <b>Message from JEE Success System</b>\n\n"
                    f"{message_text}"
                ),
                parse_mode=ParseMode.HTML,
            )
            sent += 1
        except Exception as e:
            logger.warning(f"[broadcast] Failed to send to {uid}: {e}")
            failed += 1
        # Anti-flood delay
        await asyncio.sleep(config.BROADCAST_DELAY)

    elapsed = round(time.time() - start, 1)
    await status_msg.edit_text(
        f"✅ <b>Broadcast Complete</b>\n\n"
        f"✅ Sent: {sent}\n"
        f"❌ Failed: {failed}\n"
        f"⏱ Time taken: {elapsed}s",
        parse_mode=ParseMode.HTML,
    )
    context.user_data.pop("broadcast_text", None)


# ─────────────────────────────────────────────────────────────────────────────
# User stats (detailed)
# ─────────────────────────────────────────────────────────────────────────────

async def show_user_stats(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    users = storage.list_all_users()

    total   = len(users)
    setup   = sum(1 for u in users if u.get("setup_complete"))
    streak1 = sum(1 for u in users if u.get("streak", 0) >= 1)
    streak7 = sum(1 for u in users if u.get("streak", 0) >= 7)
    streak30= sum(1 for u in users if u.get("streak", 0) >= 30)

    phases = {"beginner": 0, "intermediate": 0, "advanced": 0}
    for u in users:
        p = u.get("phase", "beginner")
        phases[p] = phases.get(p, 0) + 1

    targets = {}
    for u in users:
        y = str(u.get("target_year", "unknown"))
        targets[y] = targets.get(y, 0) + 1
    target_lines = "\n".join(f"  JEE {k}: {v}" for k, v in sorted(targets.items()))

    await query.message.reply_text(
        f"📊 <b>USER STATISTICS</b>\n\n"
        f"👥 Total: {total}\n"
        f"✅ Setup complete: {setup}\n\n"
        f"🔥 <b>Streak Breakdown</b>\n"
        f"  1+ days: {streak1}\n"
        f"  7+ days: {streak7}\n"
        f"  30+ days: {streak30}\n\n"
        f"🌱 <b>Phase Breakdown</b>\n"
        f"  Beginner: {phases['beginner']}\n"
        f"  Intermediate: {phases['intermediate']}\n"
        f"  Advanced: {phases['advanced']}\n\n"
        f"🎯 <b>Target Year</b>\n{target_lines}",
        parse_mode=ParseMode.HTML,
    )


async def show_user_list(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    users = storage.list_all_users()
    if not users:
        await query.message.reply_text("No users yet.")
        return

    # Sort by streak descending
    users.sort(key=lambda u: u.get("streak", 0), reverse=True)

    lines = []
    for i, u in enumerate(users[:20], 1):   # show top 20
        streak = u.get("streak", 0)
        phase  = u.get("phase", "b")[0].upper()
        lines.append(
            f"{i}. {u.get('name', '?')} | 🔥{streak} | {phase} | "
            f"JEE {u.get('target_year', '?')}"
        )

    text = (
        f"👥 <b>TOP USERS (by streak)</b>\n"
        f"Showing {min(20, len(users))}/{len(users)}\n\n"
        + "\n".join(lines)
    )
    await query.message.reply_text(text, parse_mode=ParseMode.HTML)


async def show_analytics(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    a     = storage.get_analytics()
    cmds  = a.get("commands", {})
    daily = a.get("daily_active", {})

    top_cmds = sorted(cmds.items(), key=lambda x: x[1], reverse=True)[:10]
    cmd_text = "\n".join(f"  /{k}: {v}" for k, v in top_cmds) or "  None"

    # Last 7 days activity
    from datetime import date, timedelta
    days_text = ""
    for i in range(6, -1, -1):
        d = str(date.today() - timedelta(days=i))
        cnt = daily.get(d, 0)
        bar = "█" * min(int(cnt / 5), 20)
        days_text += f"  {d[-5:]}: {bar} {cnt}\n"

    await query.message.reply_text(
        f"📈 <b>ANALYTICS</b>\n\n"
        f"📨 Total messages: {a.get('total_messages', 0)}\n\n"
        f"🔝 <b>Top Commands</b>\n{cmd_text}\n\n"
        f"📅 <b>Last 7 Days Activity</b>\n{days_text}",
        parse_mode=ParseMode.HTML,
    )


# ─────────────────────────────────────────────────────────────────────────────
# /addadmin  /removeadmin
# ─────────────────────────────────────────────────────────────────────────────

async def cmd_addadmin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await require_admin(update):
        return
    args = context.args
    if not args or not args[0].isdigit():
        await update.message.reply_text(
            "Usage: <code>/addadmin 123456789</code>\n"
            "(Use numeric user ID, not username)",
            parse_mode=ParseMode.HTML,
        )
        return
    new_id = int(args[0])
    config.ADMIN_IDS.add(new_id)
    await update.message.reply_text(
        f"✅ User <code>{new_id}</code> added as admin.\n"
        f"Note: This only lasts until bot restart. "
        f"To make permanent, add to ADMIN_IDS env var.",
        parse_mode=ParseMode.HTML,
    )
    logger.info(f"[admin] {new_id} added as admin by {update.effective_user.id}")


async def cmd_removeadmin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await require_admin(update):
        return
    args = context.args
    if not args or not args[0].isdigit():
        await update.message.reply_text(
            "Usage: <code>/removeadmin 123456789</code>",
            parse_mode=ParseMode.HTML,
        )
        return
    rem_id = int(args[0])
    config.ADMIN_IDS.discard(rem_id)
    await update.message.reply_text(f"✅ User <code>{rem_id}</code> removed from admins.",
                                     parse_mode=ParseMode.HTML)


# ─────────────────────────────────────────────────────────────────────────────
# ADMIN CALLBACK ROUTER — called from main callback_router
# ─────────────────────────────────────────────────────────────────────────────

async def handle_admin_callback(query, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Handles all admin_ callbacks.
    Returns True if handled, False if not an admin callback.
    """
    data = query.data

    if not data.startswith("admin_"):
        return False

    if not is_admin(query.from_user):
        await query.answer("⛔ Admins only.", show_alert=True)
        return True

    if data == "admin_broadcast":
        await query.message.reply_text(
            "📢 <b>Broadcast</b>\n\nUse command:\n"
            "<code>/broadcast Your message here</code>",
            parse_mode=ParseMode.HTML,
        )

    elif data == "admin_broadcast_confirm":
        await execute_broadcast(query, context)

    elif data == "admin_broadcast_cancel":
        context.user_data.pop("broadcast_text", None)
        await query.message.reply_text("❌ Broadcast cancelled.")

    elif data == "admin_stats":
        await show_user_stats(query, context)

    elif data == "admin_users":
        await show_user_list(query, context)

    elif data == "admin_analytics":
        await show_analytics(query, context)

    return True
