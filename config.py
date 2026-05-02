"""
config.py — Central configuration for JEE Success System Bot
All API keys, admin IDs, and settings live here.
"""
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env file locally; on Render use environment variables

# ── Telegram ─────────────────────────────────────────────────────────────────
BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "")

# ── Admin user IDs (Telegram numeric user IDs, NOT usernames) ────────────────
# To find your numeric ID: message @userinfobot on Telegram
# @radheshyam001 and @IamPranjal09 — replace with real numeric IDs below
# You can also set ADMIN_IDS as comma-separated env var: "123456,789012"
_env_admins = os.environ.get("ADMIN_IDS", "")
ADMIN_IDS: set[int] = set()
if _env_admins:
    for _id in _env_admins.split(","):
        try:
            ADMIN_IDS.add(int(_id.strip()))
        except ValueError:
            pass

# Hardcoded fallback admins (numeric IDs) — fill these in
# Example: ADMIN_IDS.add(123456789)
# NOTE: Usernames can change; numeric IDs never do.
# To get your ID: open Telegram → message @userinfobot → it replies with your ID
ADMIN_USERNAMES = {"radheshyam001", "IamPranjal09"}  # used as secondary check

# ── Google Gemini API ─────────────────────────────────────────────────────────
GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL   = "gemini-1.5-flash"          # fast & free-tier friendly
GEMINI_TIMEOUT = 20                           # seconds

# ── Rate limiting ─────────────────────────────────────────────────────────────
DOUBT_COOLDOWN_SECONDS = 30    # min seconds between doubt requests per user
MAX_DOUBT_LENGTH       = 500   # max characters in a doubt question
BROADCAST_DELAY        = 0.05  # seconds between broadcast messages (anti-flood)

# ── Images (Telegram file_ids — auto-cached after first send) ─────────────────
IMAGES: dict[str, str] = {
    "home":      os.environ.get("IMG_HOME", ""),
    "task":      os.environ.get("IMG_TASK", ""),
    "progress":  os.environ.get("IMG_PROGRESS", ""),
    "plan":      os.environ.get("IMG_PLAN", ""),
    "resources": os.environ.get("IMG_RESOURCES", ""),
    "earn":      os.environ.get("IMG_EARN", ""),
    "welcome":   os.environ.get("IMG_WELCOME", ""),
}
IMG_LOCAL: dict[str, str] = {
    "home":      "images/home.png",
    "task":      "images/task.png",
    "progress":  "images/progress.png",
    "plan":      "images/plan.png",
    "resources": "images/resources.png",
    "earn":      "images/earn.png",
    "welcome":   "images/welcome.png",
}

# ── Flask keep-alive ──────────────────────────────────────────────────────────
PORT = int(os.environ.get("PORT", 10000))

# ── Analytics log file ────────────────────────────────────────────────────────
ANALYTICS_FILE = "data/analytics.json"
