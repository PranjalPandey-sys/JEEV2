"""
storage.py — User data persistence (JSON files, zero external dependencies)
Each user gets data/user_{id}.json
Analytics stored in data/analytics.json
"""
import json
import random
from datetime import date, datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# LOW-LEVEL helpers
# ─────────────────────────────────────────────────────────────────────────────

def _user_file(user_id: int) -> Path:
    return DATA_DIR / f"user_{user_id}.json"

def _load(user_id: int) -> dict:
    fp = _user_file(user_id)
    if fp.exists():
        try:
            return json.loads(fp.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}

def _save(user_id: int, data: dict) -> None:
    _user_file(user_id).write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )

# ─────────────────────────────────────────────────────────────────────────────
# USER CRUD
# ─────────────────────────────────────────────────────────────────────────────

def get_user(user_id: int) -> dict | None:
    data = _load(user_id)
    return data if data else None

def create_user(user_id: int, name: str, target_year: int = 2026) -> dict:
    user = {
        "user_id": user_id,
        "name": name,
        "target_year": target_year,
        "joined_date": str(date.today()),
        "current_day": 1,
        "current_week": 1,
        "streak": 0,
        "best_streak": 0,
        "last_active": str(date.today()),
        "total_study_hours": 0.0,
        "tasks_completed": 0,
        "tasks_total": 0,
        "daily_goal_hours": 1.0,
        "completed_days": [],
        "missed_days": [],
        "subject_progress": {
            "physics":   {"completed_topics": 0, "total_topics": 50},
            "chemistry": {"completed_topics": 0, "total_topics": 50},
            "maths":     {"completed_topics": 0, "total_topics": 50},
        },
        "completed_chapters": [],
        "today_task_done": False,
        "today_task_date": "",
        "phase": "beginner",
        "notifications_enabled": True,
        "setup_complete": False,
        "doubt_last_asked": "",   # ISO datetime string for rate-limiting
    }
    _save(user_id, user)
    return user

def update_user(user_id: int, **kwargs) -> dict:
    data = _load(user_id)
    data.update(kwargs)
    _save(user_id, data)
    return data

def list_all_users() -> list[dict]:
    """Return list of all user dicts (for admin panel)."""
    users = []
    for fp in DATA_DIR.glob("user_*.json"):
        try:
            users.append(json.loads(fp.read_text(encoding="utf-8")))
        except Exception:
            pass
    return users

def get_all_user_ids() -> list[int]:
    return [u["user_id"] for u in list_all_users() if "user_id" in u]

# ─────────────────────────────────────────────────────────────────────────────
# STREAK logic
# ─────────────────────────────────────────────────────────────────────────────

def mark_task_done(user_id: int) -> dict:
    data = _load(user_id)
    today = str(date.today())

    if data.get("today_task_done") and data.get("today_task_date") == today:
        return data  # already done today

    data["today_task_done"] = True
    data["today_task_date"] = today
    data["tasks_completed"] = data.get("tasks_completed", 0) + 1

    last_active = data.get("last_active", "")
    yesterday   = str(date.today() - timedelta(days=1))

    if last_active in (yesterday, today):
        data["streak"] = data.get("streak", 0) + 1
    else:
        data["streak"] = 1  # restart

    data["best_streak"] = max(data.get("best_streak", 0), data["streak"])
    data["last_active"]  = today

    if today not in data.get("completed_days", []):
        data.setdefault("completed_days", []).append(today)

    data["total_study_hours"] = round(
        data.get("total_study_hours", 0) + data.get("daily_goal_hours", 1.0), 1
    )

    data["current_day"] = data.get("current_day", 1) + 1
    if data["current_day"] % 7 == 1:
        data["current_week"] = data.get("current_week", 1) + 1

    # Gradual goal escalation
    day = data["current_day"]
    if   day <=  7: goal, phase = 1.0, "beginner"
    elif day <= 14: goal, phase = 1.5, "beginner"
    elif day <= 21: goal, phase = 2.0, "intermediate"
    elif day <= 30: goal, phase = 2.5, "intermediate"
    elif day <= 45: goal, phase = 3.5, "intermediate"
    else:           goal, phase = 5.0, "advanced"

    data["daily_goal_hours"] = goal
    data["phase"]             = phase

    _save(user_id, data)
    return data

def handle_missed_day(user_id: int) -> dict:
    data = _load(user_id)
    yesterday = str(date.today() - timedelta(days=1))
    today     = str(date.today())

    last = data.get("last_active", "")
    if last and last != yesterday and last != today:
        data["daily_goal_hours"] = max(1.0, data.get("daily_goal_hours", 1.0) - 0.5)
        data["streak"]           = 0
        if yesterday not in data.get("missed_days", []):
            data.setdefault("missed_days", []).append(yesterday)
        _save(user_id, data)

    return data

# ─────────────────────────────────────────────────────────────────────────────
# STATS
# ─────────────────────────────────────────────────────────────────────────────

def get_stats(user_id: int) -> dict:
    data = _load(user_id)
    if not data:
        return {}

    joined        = datetime.strptime(data.get("joined_date", str(date.today())), "%Y-%m-%d").date()
    days_since    = (date.today() - joined).days + 1
    target        = date(data.get("target_year", 2026), 4, 1)
    days_left     = (target - date.today()).days

    sp            = data.get("subject_progress", {})
    phy_done      = sp.get("physics",   {}).get("completed_topics", 0)
    chem_done     = sp.get("chemistry", {}).get("completed_topics", 0)
    math_done     = sp.get("maths",     {}).get("completed_topics", 0)
    overall_pct   = round((phy_done + chem_done + math_done) / 150 * 100, 1)

    return {
        **data,
        "days_since_join":    days_since,
        "days_left":          days_left,
        "overall_progress_pct": overall_pct,
        "avg_daily_hours":    round(data.get("total_study_hours", 0) / max(days_since, 1), 1),
    }

# ─────────────────────────────────────────────────────────────────────────────
# TASK GENERATOR
# ─────────────────────────────────────────────────────────────────────────────

def generate_today_task(user_id: int) -> dict:
    from study_data import PHYSICS_CHAPTERS, CHEMISTRY_CHAPTERS, MATHS_CHAPTERS, DAILY_TIPS, QUOTES

    data = _load(user_id)
    if not data:
        return {}

    day      = data.get("current_day", 1)
    goal_hrs = data.get("daily_goal_hours", 1.0)
    scale    = max(0.4, min(goal_hrs / 2.5, 2.0))

    def pick(lst):
        return lst[(day - 1) % len(lst)]

    def scale_task(ch):
        return {
            **ch,
            "time_min":  max(15, int(ch["time_min"]  * scale)),
            "questions": max(5,  int(ch["questions"] * scale)),
        }

    tasks = {
        "physics":   scale_task(pick(PHYSICS_CHAPTERS)),
        "chemistry": scale_task(pick(CHEMISTRY_CHAPTERS)),
        "maths":     scale_task(pick(MATHS_CHAPTERS)),
    }

    return {
        "day":            day,
        "week":           data.get("current_week", 1),
        "streak":         data.get("streak", 0),
        "goal_hours":     goal_hrs,
        "goal_mins":      int(goal_hrs * 60),
        "tasks":          tasks,
        "total_task_time": sum(t["time_min"] for t in tasks.values()),
        "tip":            random.choice(DAILY_TIPS),
        "quote":          random.choice(QUOTES),
        "phase":          data.get("phase", "beginner"),
    }

# ─────────────────────────────────────────────────────────────────────────────
# ANALYTICS
# ─────────────────────────────────────────────────────────────────────────────

_ANALYTICS_FILE = DATA_DIR / "analytics.json"

def _load_analytics() -> dict:
    if _ANALYTICS_FILE.exists():
        try:
            return json.loads(_ANALYTICS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"commands": {}, "total_messages": 0, "daily_active": {}}

def _save_analytics(data: dict) -> None:
    _ANALYTICS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def log_command(command: str) -> None:
    """Increment command usage counter."""
    try:
        a = _load_analytics()
        a["commands"][command] = a["commands"].get(command, 0) + 1
        a["total_messages"]    = a.get("total_messages", 0) + 1
        today = str(date.today())
        a.setdefault("daily_active", {})[today] = a["daily_active"].get(today, 0) + 1
        _save_analytics(a)
    except Exception:
        pass  # analytics must never crash the bot

def get_analytics() -> dict:
    return _load_analytics()

# ─────────────────────────────────────────────────────────────────────────────
# DOUBT rate-limiting helpers
# ─────────────────────────────────────────────────────────────────────────────

def can_ask_doubt(user_id: int, cooldown_seconds: int = 30) -> tuple[bool, int]:
    """Returns (allowed, seconds_remaining)."""
    data = _load(user_id)
    last = data.get("doubt_last_asked", "")
    if not last:
        return True, 0
    try:
        last_dt  = datetime.fromisoformat(last)
        elapsed  = (datetime.now() - last_dt).total_seconds()
        if elapsed >= cooldown_seconds:
            return True, 0
        return False, int(cooldown_seconds - elapsed)
    except Exception:
        return True, 0

def record_doubt_asked(user_id: int) -> None:
    update_user(user_id, doubt_last_asked=datetime.now().isoformat())
