"""
handlers/tasks.py
Today's Task — personalised daily study plan.
"""
import logging
import random
from datetime import date

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import storage
import study_data
from handlers.helpers import send_screen, back_home_keyboard

logger = logging.getLogger(__name__)


async def show_task(source, context: ContextTypes.DEFAULT_TYPE, uid: int = None) -> None:
    if uid is None:
        uid = (
            source.from_user.id if hasattr(source, "from_user")
            else source.effective_user.id
        )

    task_data = storage.generate_today_task(uid)
    if not task_data:
        return

    user      = storage.get_user(uid)
    t         = task_data["tasks"]
    phy       = t["physics"]
    chem      = t["chemistry"]
    maths     = t["maths"]
    done_today = (
        user.get("today_task_done")
        and user.get("today_task_date") == str(date.today())
    )

    caption = (
        f"📅 <b>TODAY'S TASK — Day {task_data['day']}</b>  "
        f"🔥 <b>{task_data['streak']} Day Streak</b>\n\n"

        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚛️ <b>PHYSICS</b> — {phy['name']}\n"
        f"   📖 {', '.join(phy['topics'][:2])}\n"
        f"   ⏱ {phy['time_min']} min  |  🎯 {phy['questions']} questions\n"
        f"   📚 {phy['pyq_range']}\n"
        f"   💡 <i>{phy['tip']}</i>\n\n"

        f"🧪 <b>CHEMISTRY</b> — {chem['name']}\n"
        f"   📖 {', '.join(chem['topics'][:2])}\n"
        f"   ⏱ {chem['time_min']} min  |  🎯 {chem['questions']} questions\n"
        f"   📚 {chem['pyq_range']}\n"
        f"   💡 <i>{chem['tip']}</i>\n\n"

        f"📐 <b>MATHS</b> — {maths['name']}\n"
        f"   📖 {', '.join(maths['topics'][:2])}\n"
        f"   ⏱ {maths['time_min']} min  |  🎯 {maths['questions']} questions\n"
        f"   📚 {maths['pyq_range']}\n"
        f"   💡 <i>{maths['tip']}</i>\n\n"

        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"⏰ Total: <b>{task_data['total_task_time']} min</b>  "
        f"|  Goal: <b>{task_data['goal_hours']} hrs</b>\n\n"
        f"📌 <i>{task_data['tip']}</i>\n"
        f"✨ <i>{task_data['quote']}</i>"
    )

    if done_today:
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Completed Today! Great work 🏆", callback_data="noop")],
            [InlineKeyboardButton("🏠 Back to Home", callback_data="home")],
        ])
    else:
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Mark as Completed!", callback_data="mark_done")],
            [InlineKeyboardButton("🏠 Back to Home", callback_data="home")],
        ])

    await send_screen(source, context, "task", caption, kb)


async def handle_mark_done(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid  = query.from_user.id
    data = storage.mark_task_done(uid)

    streak = data.get("streak", 1)
    goal   = data.get("daily_goal_hours", 1.0)
    phase  = data.get("phase", "beginner")
    quote  = random.choice(study_data.QUOTES)

    # Achievement unlocks
    milestone = ""
    if   streak == 7:  milestone = "\n\n🏅 <b>Achievement Unlocked: 7-Day Streak!</b>"
    elif streak == 14: milestone = "\n\n🥈 <b>Achievement Unlocked: 14-Day Streak!</b>"
    elif streak == 30: milestone = "\n\n🥇 <b>Achievement Unlocked: 30-Day Streak! Legend! 🔥</b>"
    elif streak == 50: milestone = "\n\n💎 <b>50-Day Streak — You are UNSTOPPABLE!</b>"
    elif streak == 100:milestone = "\n\n👑 <b>100-Day Streak — Future IITian confirmed! 🎓</b>"

    await query.answer("✅ Task marked as completed! Great work!", show_alert=False)
    await query.message.reply_text(
        f"🎉 <b>Task Completed! Day {data.get('current_day', 1) - 1}</b>\n\n"
        f"🔥 <b>Streak: {streak} day{'s' if streak != 1 else ''}!</b>  "
        f"{'🔥' * min(streak, 5)}\n"
        f"⏱ Study logged: <b>{goal} hr{'s' if goal != 1 else ''}</b>\n"
        f"📈 Phase: <b>{phase.capitalize()}</b>\n"
        f"{milestone}\n\n"
        f"<i>{quote}</i>\n\n"
        f"See you tomorrow — keep the streak alive! 💪",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📊 View Progress", callback_data="progress")],
            [InlineKeyboardButton("🏠 Home",          callback_data="home")],
        ]),
    )


async def cmd_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    storage.log_command("task")
    await show_task(update, context, uid=update.effective_user.id)
