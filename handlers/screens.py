"""
handlers/screens.py
All remaining screen handlers:
  - Progress
  - Full Plan
  - Study Resources
  - Earn While You Learn
  - Settings
  - Doubt (AI Tutor entry)
  - Streak command
  - Help command
"""
import logging
import random
from datetime import date

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import storage
import study_data
from handlers.helpers import (
    send_screen, back_home_keyboard, progress_bar, phase_emoji
)

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# MY PROGRESS
# ─────────────────────────────────────────────────────────────────────────────

async def show_progress(source, context: ContextTypes.DEFAULT_TYPE, uid: int = None) -> None:
    if uid is None:
        uid = source.from_user.id if hasattr(source, "from_user") else source.effective_user.id

    stats = storage.get_stats(uid)
    if not stats:
        return

    sp       = stats.get("subject_progress", {})
    phy_pct  = round(sp.get("physics",   {}).get("completed_topics", 0) / 50 * 100)
    chem_pct = round(sp.get("chemistry", {}).get("completed_topics", 0) / 50 * 100)
    math_pct = round(sp.get("maths",     {}).get("completed_topics", 0) / 50 * 100)
    overall  = stats.get("overall_progress_pct", 0)

    streak = stats.get("streak", 0)
    best   = stats.get("best_streak", 0)
    phase  = stats.get("phase", "beginner")

    achievements = []
    if streak >= 7:   achievements.append("🏅 7-Day Streak — Great consistency!")
    if streak >= 14:  achievements.append("🥈 14-Day Streak — On fire!")
    if streak >= 30:  achievements.append("🥇 30-Day Streak — Unstoppable!")
    if stats.get("total_study_hours", 0) >= 10: achievements.append("⚡ 10+ Study Hours logged")
    if stats.get("tasks_completed", 0)   >= 10: achievements.append("🎯 10 Tasks Completed")
    if not achievements:
        achievements = ["Keep going to unlock your first achievement! 💪"]

    caption = (
        f"📊 <b>MY PROGRESS</b>\n\n"
        f"🔥 <b>Streak:</b> {streak} days  (Best: {best})\n"
        f"⏱ <b>Total Study:</b> {stats.get('total_study_hours', 0)} hrs\n"
        f"✅ <b>Tasks Done:</b> {stats.get('tasks_completed', 0)}\n"
        f"📅 <b>Avg Daily:</b> {stats.get('avg_daily_hours', 0)} hrs\n"
        f"⏳ <b>Days Left:</b> {stats.get('days_left', 365)} to JEE\n\n"

        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"📚 <b>Subject Progress</b>\n"
        f"⚛️ Physics    {progress_bar(phy_pct)}  <b>{phy_pct}%</b>\n"
        f"🧪 Chemistry  {progress_bar(chem_pct)}  <b>{chem_pct}%</b>\n"
        f"📐 Maths      {progress_bar(math_pct)}  <b>{math_pct}%</b>\n\n"
        f"🌟 <b>Overall:</b> {progress_bar(overall)}  <b>{overall}%</b>\n\n"

        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🏆 <b>Achievements</b>\n"
        + "\n".join(f"  • {a}" for a in achievements[:4]) +
        f"\n\n{phase_emoji(phase)} Phase: <b>{phase.capitalize()}</b>  "
        f"| Goal: <b>{stats.get('daily_goal_hours', 1)} hrs/day</b>"
    )

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Back to Home", callback_data="home")]
    ])
    await send_screen(source, context, "progress", caption, kb)


async def cmd_progress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    storage.log_command("progress")
    await show_progress(update, context, uid=update.effective_user.id)


# ─────────────────────────────────────────────────────────────────────────────
# FULL PLAN
# ─────────────────────────────────────────────────────────────────────────────

async def show_plan(source, context: ContextTypes.DEFAULT_TYPE,
                    uid: int = None, week: int = None) -> None:
    if uid is None:
        uid = source.from_user.id if hasattr(source, "from_user") else source.effective_user.id

    user = storage.get_user(uid)
    if not user:
        return

    current_week = user.get("current_week", 1)
    if week is None:
        week = current_week

    week    = max(1, min(week, 12))
    chapters = study_data.get_chapters_by_week(week)

    def fmt(lst):
        if not lst:
            return "  • Advanced/custom topics\n"
        return "".join(f"  • {c['name']} ({c['time_min']} min)\n" for c in lst)

    days_left = (date(user.get("target_year", 2026), 4, 1) - date.today()).days
    overall   = storage.get_stats(uid).get("overall_progress_pct", 0)

    caption = (
        f"🗺️ <b>YOUR FULL PLAN</b>\n\n"
        f"📅 Week <b>{week}</b>  (You are on Week <b>{current_week}</b>)\n"
        f"⏳ <b>{days_left} days</b> left  |  🌟 <b>{overall}%</b> complete\n\n"

        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚛️ <b>PHYSICS — Week {week}</b>\n" + fmt(chapters["phy"]) +
        f"\n🧪 <b>CHEMISTRY — Week {week}</b>\n" + fmt(chapters["chem"]) +
        f"\n📐 <b>MATHS — Week {week}</b>\n" + fmt(chapters["math"]) +

        f"\n━━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 <b>Plan Highlights</b>\n"
        f"  ✅ Balanced across all 3 subjects\n"
        f"  ✅ Concept → Practice → Test\n"
        f"  ✅ Weekly mini-tests from Week 3\n\n"
        f"<i>Stick to the plan. Small daily steps = big results! 🚀</i>"
    )

    nav = []
    if week > 1:
        nav.append(InlineKeyboardButton(f"◀ Week {week - 1}", callback_data=f"plan_week_{week - 1}"))
    if week < 12:
        nav.append(InlineKeyboardButton(f"Week {week + 1} ▶", callback_data=f"plan_week_{week + 1}"))

    kb = InlineKeyboardMarkup([
        nav,
        [InlineKeyboardButton("📅 Today's Task", callback_data="task")],
        [InlineKeyboardButton("🏠 Back to Home",  callback_data="home")],
    ])
    await send_screen(source, context, "plan", caption, kb)


async def cmd_plan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    storage.log_command("plan")
    await show_plan(update, context, uid=update.effective_user.id)


# ─────────────────────────────────────────────────────────────────────────────
# STUDY RESOURCES  (tabbed: PYQs / Books / Mocks)
# ─────────────────────────────────────────────────────────────────────────────

_RES_PAGES = {
    "pyq": (
        "📚 <b>STUDY RESOURCES — Previous Year Questions</b>\n\n"
        "📘 <b>OSWAAL JEE PYQs (2023–2002)</b>\n"
        "  • Chapter + topic-wise organisation\n"
        "  • Physics, Chemistry, Mathematics\n"
        "  • Detailed solutions included\n"
        "  ✅ <b>How to use:</b> After each chapter, solve Oswaal PYQs "
        "for that chapter (10–20 Qs). Never skip the solutions!\n\n"
        "📗 <b>ARIHANT Chapterwise PYQs</b>\n"
        "  • Year-wise papers 2002–2023\n"
        "  ✅ <b>How to use:</b> Full paper every Sunday. "
        "Analyse mistakes on Monday morning.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "🎯 <b>Daily PYQ Habit:</b>\n"
        "  • 5 PYQs per topic = 15 PYQs/day minimum\n"
        "  • Start from 2023, go backwards\n"
        "  • Mark difficult ones for weekly revision\n\n"
        "💡 <i>JEE repeats 30–40% of patterns every year. PYQs are GOLD.</i>"
    ),
    "books": (
        "📚 <b>STUDY RESOURCES — Recommended Books</b>\n\n"
        "⚛️ <b>PHYSICS</b>\n"
        "  📗 NCERT XI + XII — read first, always\n"
        "  📘 HC Verma — Concepts of Physics (Vol 1 & 2)\n"
        "     ↳ Solve exercises: 20 Qs/chapter minimum\n"
        "  📙 Arihant DC Pandey — JEE-level practice\n\n"
        "🧪 <b>CHEMISTRY</b>\n"
        "  📗 NCERT XI + XII — mandatory base\n"
        "  📘 OP Tandon — Inorganic (p/d/f block)\n"
        "  📙 MS Chauhan — Organic reactions\n"
        "  📕 Narendra Awasthi — Physical numericals\n\n"
        "📐 <b>MATHEMATICS</b>\n"
        "  📗 NCERT XI + XII — examples first!\n"
        "  📘 RD Sharma — concept building\n"
        "  📙 Arihant Skills in Maths series\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "📌 <i>Quality over quantity. One book fully done > "
        "three books partially done.</i>"
    ),
    "mock": (
        "📚 <b>STUDY RESOURCES — Mock Tests</b>\n\n"
        "🔰 <b>WHEN TO START</b>\n"
        "  • Chapter tests: After each chapter\n"
        "  • Full mocks: From Week 3 onwards\n"
        "  • Full-syllabus mocks: Last 60 days\n\n"
        "📝 <b>CHAPTER MINI TESTS</b>\n"
        "  • 15 questions per chapter, 20 minutes\n"
        "  • Use Oswaal chapter tests\n\n"
        "📊 <b>FREE ONLINE FULL MOCKS</b>\n"
        "  • NTA Official: jeemain.nta.nic.in\n"
        "  • Allen/Resonance DPPs (free)\n"
        "  • Embibe, Unacademy free tests\n\n"
        "🏆 <b>TEST STRATEGY</b>\n"
        "  1. Attempt in full exam conditions\n"
        "  2. Log every wrong answer\n"
        "  3. Re-study that topic next day\n"
        "  4. Reattempt wrong Qs within 48 hrs\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "⚡ <i>Every wrong answer in a mock = one less mistake in the real exam.</i>"
    ),
}

def _res_keyboard(active: str) -> InlineKeyboardMarkup:
    tabs = []
    for key, label in [("pyq", "📄 PYQs"), ("books", "📖 Books"), ("mock", "🎯 Mocks")]:
        text = f"▶ {label}" if key == active else label
        tabs.append(InlineKeyboardButton(text, callback_data=f"res_{key}"))
    return InlineKeyboardMarkup([
        tabs,
        [InlineKeyboardButton("🏠 Back to Home", callback_data="home")],
    ])

async def show_resources(source, context: ContextTypes.DEFAULT_TYPE,
                         page: str = "pyq", uid: int = None) -> None:
    caption = _RES_PAGES.get(page, _RES_PAGES["pyq"])
    await send_screen(source, context, "resources", caption, _res_keyboard(page))

async def cmd_resources(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    storage.log_command("resources")
    await show_resources(update, context)


# ─────────────────────────────────────────────────────────────────────────────
# EARN WHILE YOU LEARN
# ─────────────────────────────────────────────────────────────────────────────

async def show_earn(source, context: ContextTypes.DEFAULT_TYPE,
                    gig_idx: int = -1, uid: int = None) -> None:
    gigs = study_data.EARNING_GIGS

    if gig_idx == -1:
        # Overview
        lines = ""
        for i, g in enumerate(gigs):
            lines += f"{i+1}. {g['title']}\n   💸 {g['earning']}  |  ⏱ {g['time']}  |  {g['demand']}\n\n"

        caption = (
            "💰 <b>EARN WHILE YOU LEARN</b>\n\n"
            "<i>Build skills. Earn money. Support your JEE journey.</i>\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "⚡ <b>Top 5 Student-Friendly Gigs</b>\n\n"
            + lines +
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "📌 <b>Rule:</b> Max 1–2 hours/day on earning.\n"
            "<i>JEE is your primary mission!</i>"
        )

        gig_btns = [
            InlineKeyboardButton(f"{i+1}. {g['title'][:18]}", callback_data=f"earn_{i}")
            for i, g in enumerate(gigs)
        ]
        rows = [gig_btns[i:i+2] for i in range(0, len(gig_btns), 2)]
        rows.append([InlineKeyboardButton("🏠 Back to Home", callback_data="home")])
        kb = InlineKeyboardMarkup(rows)

    else:
        g         = gigs[gig_idx]
        steps_txt = "\n".join(g["steps"])
        caption   = (
            f"{g['title']}\n\n"
            f"📋 <b>What you'll do:</b> {g['desc']}\n\n"
            f"💸 <b>Earning:</b> {g['earning']}\n"
            f"⏱ <b>Time:</b> {g['time']}\n"
            f"🔑 <b>Skill:</b> {g['skill']}\n"
            f"📈 <b>Demand:</b> {g['demand']}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🚀 <b>Step-by-Step: How to Start Today</b>\n\n"
            f"{steps_txt}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"⚠️ <b>Remember:</b> Max 1–2 hrs/day. JEE = Priority #1."
        )
        nav = []
        if gig_idx > 0:
            nav.append(InlineKeyboardButton("◀ Prev", callback_data=f"earn_{gig_idx - 1}"))
        if gig_idx < len(gigs) - 1:
            nav.append(InlineKeyboardButton("Next ▶", callback_data=f"earn_{gig_idx + 1}"))

        kb = InlineKeyboardMarkup([
            nav,
            [InlineKeyboardButton("📋 All Gigs", callback_data="earn")],
            [InlineKeyboardButton("🏠 Back to Home", callback_data="home")],
        ])

    await send_screen(source, context, "earn", caption, kb)

async def cmd_earn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    storage.log_command("earn")
    await show_earn(update, context, uid=update.effective_user.id)


# ─────────────────────────────────────────────────────────────────────────────
# SETTINGS
# ─────────────────────────────────────────────────────────────────────────────

async def show_settings(source, context: ContextTypes.DEFAULT_TYPE, uid: int = None) -> None:
    if uid is None:
        uid = source.from_user.id if hasattr(source, "from_user") else source.effective_user.id

    user = storage.get_user(uid)
    if not user:
        return

    notif  = "✅ ON" if user.get("notifications_enabled", True) else "❌ OFF"
    toggle = ("🔕 Turn OFF Notifications" if user.get("notifications_enabled", True)
               else "🔔 Turn ON Notifications")

    caption = (
        f"⚙️ <b>SETTINGS</b>\n\n"
        f"👤 Name: <b>{user['name']}</b>\n"
        f"🎯 Target: <b>JEE {user.get('target_year', 2026)}</b>\n"
        f"📅 Joined: <b>{user.get('joined_date', 'N/A')}</b>\n"
        f"🌱 Phase: <b>{user.get('phase', 'beginner').capitalize()}</b>\n"
        f"⏱ Daily Goal: <b>{user.get('daily_goal_hours', 1)} hrs</b>\n"
        f"🔔 Notifications: <b>{notif}</b>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>Your daily goal increases automatically as you progress.\n"
        f"Beginner: 1 hr → Intermediate: 2.5 hrs → Advanced: 5 hrs</i>"
    )

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(toggle,               callback_data="toggle_notif")],
        [InlineKeyboardButton("🔄 Reset Progress",  callback_data="confirm_reset")],
        [InlineKeyboardButton("🏠 Back to Home",    callback_data="home")],
    ])
    await send_screen(source, context, "home", caption, kb)


async def handle_toggle_notif(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid     = query.from_user.id
    user    = storage.get_user(uid)
    current = user.get("notifications_enabled", True)
    storage.update_user(uid, notifications_enabled=not current)
    await show_settings(query, context, uid=uid)


async def handle_confirm_reset(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    await query.message.reply_text(
        "⚠️ <b>Are you sure?</b>\n\n"
        "This will reset ALL your progress, streaks and data.\n"
        "This action <b>cannot be undone</b>.",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("⚠️ Yes, Reset", callback_data="do_reset"),
            InlineKeyboardButton("❌ Cancel",      callback_data="settings"),
        ]]),
    )

async def handle_do_reset(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid  = query.from_user.id
    user = storage.get_user(uid)
    storage.create_user(uid, user.get("name", "Aspirant"), user.get("target_year", 2026))
    storage.update_user(uid, setup_complete=True)
    await query.message.reply_text(
        "✅ Progress reset. Starting fresh!\n\nType /start to begin again.",
        parse_mode=ParseMode.HTML,
    )


# ─────────────────────────────────────────────────────────────────────────────
# DOUBT ENTRY (AI Tutor)
# ─────────────────────────────────────────────────────────────────────────────

async def show_doubt_prompt(source, context: ContextTypes.DEFAULT_TYPE, uid: int = None) -> None:
    """Tell user to type their question. Actual solving is in handlers/doubt.py."""
    caption = (
        "🤖 <b>JEE AI Tutor — Powered by Gemini</b>\n\n"
        "Ask any JEE-level doubt in Physics, Chemistry, or Mathematics.\n\n"
        "📝 <b>Just type your question</b> and I'll solve it step-by-step!\n\n"
        "Examples:\n"
        "  • 'What is Gauss's Law and when do I use it?'\n"
        "  • 'How to solve projectile motion problems?'\n"
        "  • 'Explain Mole Concept with an example'\n\n"
        "⚠️ Max 500 characters per question\n"
        "⏱ 30-second cooldown between questions\n\n"
        "<i>Powered by Google Gemini AI 🧠</i>"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Back to Home", callback_data="home")]
    ])
    # Set state so next message is treated as doubt question
    context.user_data["awaiting_doubt"] = True
    await send_screen(source, context, "home", caption, kb)


# ─────────────────────────────────────────────────────────────────────────────
# STREAK command
# ─────────────────────────────────────────────────────────────────────────────

async def cmd_streak(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    storage.log_command("streak")
    uid   = update.effective_user.id
    stats = storage.get_stats(uid)
    if not stats:
        await update.message.reply_text("Please /start first.")
        return

    streak = stats.get("streak", 0)
    best   = stats.get("best_streak", 0)
    fire   = "🔥" * min(streak, 10) if streak else "❄️ No streak yet — start today!"

    await update.message.reply_text(
        f"🔥 <b>Your Streak</b>\n\n"
        f"Current: <b>{streak} days</b>  {fire}\n"
        f"Best ever: <b>{best} days</b>\n\n"
        f"<i>{random.choice(study_data.QUOTES)}</i>",
        parse_mode=ParseMode.HTML,
    )


# ─────────────────────────────────────────────────────────────────────────────
# HELP command
# ─────────────────────────────────────────────────────────────────────────────

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    storage.log_command("help")
    await update.message.reply_text(
        "📋 <b>JEE Success System — Commands</b>\n\n"
        "/start — Setup / Return to home\n"
        "/home — Dashboard\n"
        "/task — Today's task\n"
        "/progress — My progress\n"
        "/plan — Full study plan\n"
        "/resources — Study resources\n"
        "/earn — Earning opportunities\n"
        "/doubt — Ask AI tutor\n"
        "/streak — Check your streak\n"
        "/help — This message\n\n"
        "<i>Discipline today, Dreams tomorrow. 🚀</i>",
        parse_mode=ParseMode.HTML,
    )
