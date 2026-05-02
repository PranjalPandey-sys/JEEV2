# 🎓 JEE Success System — Telegram Bot

> **Plan. Execute. Succeed.**  
> A daily-use system for JEE aspirants combining structured study, progress tracking, and earning opportunities.

---

## 📁 Project Structure

```
jee_bot/
├── bot.py            ← Main bot (all handlers, Flask keep-alive)
├── storage.py        ← User data (JSON file-based, no external DB)
├── study_data.py     ← Full syllabus, earning gigs, quotes, tips
├── requirements.txt  ← Dependencies
├── .env.example      ← Environment variable template
├── data/             ← Auto-created; stores user JSON files
└── images/           ← Place your 7 PNG images here (optional)
    ├── home.png
    ├── task.png
    ├── progress.png
    ├── plan.png
    ├── resources.png
    ├── earn.png
    └── welcome.png
```

---

## ⚡ Features

| Feature | Description |
|---|---|
| 🌱 Beginner Mode | Starts at 1 hr/day, auto-scales to 5 hrs |
| 📅 Daily Task Engine | Personalised Physics/Chemistry/Maths tasks |
| 📊 Progress Tracker | Streaks, study hours, subject progress % |
| 🗺️ Full Roadmap | 8-week plan with chapter-wise breakdown |
| 📚 Study Resources | PYQs (Oswaal), Books, Mock Tests with instructions |
| 💰 Earn Section | 5 student-friendly gigs with step-by-step guides |
| 🔄 Missed Day Handler | Reduces load if user skips — prevents burnout |
| 🏆 Achievements | Unlocked for streaks, study hours, tasks |
| 🔔 Keep-Alive | Flask + UptimeRobot for Render free tier |

---

## 🚀 Deploy on Render (Free Tier)

### Step 1 — Create the Bot
1. Open [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` → follow prompts
3. Copy your **Bot Token**

### Step 2 — Push to GitHub
```bash
git init
git add .
git commit -m "JEE Success System Bot"
git remote add origin https://github.com/YOUR_USERNAME/jee-bot.git
git push -u origin main
```

### Step 3 — Deploy on Render
1. Go to [render.com](https://render.com) → New → **Web Service**
2. Connect your GitHub repo
3. Fill in:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
   - **Environment:** Python 3

### Step 4 — Set Environment Variables on Render
In Render dashboard → Environment → Add:
```
BOT_TOKEN = your_telegram_bot_token
```

### Step 5 — Add Images (optional but recommended)
Place your 7 PNG images in an `images/` folder in the repo.  
After first bot run, Telegram file_ids are auto-cached in the `IMAGES` dict.  
For production speed, copy the logged file_ids into environment variables:
```
IMG_HOME     = AgACAgI...
IMG_TASK     = AgACAgI...
IMG_PROGRESS = AgACAgI...
IMG_PLAN     = AgACAgI...
IMG_RESOURCES= AgACAgI...
IMG_EARN     = AgACAgI...
IMG_WELCOME  = AgACAgI...
```

### Step 6 — Set Up UptimeRobot
1. Go to [uptimerobot.com](https://uptimerobot.com) → Add Monitor
2. Type: HTTP(s)
3. URL: `https://your-render-app.onrender.com/`
4. Interval: Every 5 minutes

This prevents Render free tier from sleeping.

---

## 🤖 Bot Commands

| Command | Action |
|---|---|
| `/start` | Setup / Return to home |
| `/home` | Main dashboard |
| `/task` | Today's personalised task |
| `/progress` | Progress, streaks, stats |
| `/plan` | Full 8-week roadmap |
| `/resources` | PYQs, books, mock tests |
| `/earn` | Earning opportunities |
| `/streak` | Check current streak |
| `/help` | All commands |

---

## 🔧 Local Development

```bash
# 1. Clone repo
git clone https://github.com/YOUR_USERNAME/jee-bot.git
cd jee-bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variable
export BOT_TOKEN="your_token_here"

# 4. Run
python bot.py
```

---

## 📐 Architecture

```
User Message
     │
     ▼
ConversationHandler (onboarding)
     │
     ├── /start → ASK_NAME → ASK_YEAR → Home Dashboard
     │
CommandHandlers (/task, /progress, /plan ...)
     │
CallbackQueryHandler (inline buttons)
     │
     ├── show_task()      → Personalised daily task
     ├── show_progress()  → Stats + achievements  
     ├── show_plan()      → Weekly roadmap (navigable)
     ├── show_resources() → PYQs / Books / Mocks (tabbed)
     ├── show_earn()      → Gig overview + detail pages
     └── mark_done_handler() → Streak + progress update

Storage Layer (JSON files in /data/)
     └── user_{id}.json per user
```

---

## 🌱 Beginner Mode — Daily Goal Progression

| Days | Goal | Phase |
|---|---|---|
| 1–7 | 1.0 hr/day | Beginner |
| 8–14 | 1.5 hrs/day | Beginner |
| 15–21 | 2.0 hrs/day | Intermediate |
| 22–30 | 2.5 hrs/day | Intermediate |
| 31–45 | 3.5 hrs/day | Intermediate |
| 46+ | 5.0 hrs/day | Advanced |

---

## 📚 Study Resources Covered

**Physics:** HC Verma, Arihant DC Pandey, NCERT, Oswaal PYQs  
**Chemistry:** NCERT, OP Tandon, MS Chauhan, Narendra Awasthi, Oswaal PYQs  
**Mathematics:** RD Sharma, Arihant Skills series, NCERT, Oswaal PYQs

---

## 💰 Earning Gigs Included

1. Content Writing — ₹500–₹1500/task
2. Graphic Designing — ₹300–₹1000/design
3. Online Tutoring — ₹500–₹2000/hr
4. YouTube Automation — ₹1000–₹5000/project
5. Freelance Assistant — ₹300–₹800/task

Each gig includes a 5-step "Start Today" action plan.

---

## 🛡️ Error Handling

- `TimedOut` and `NetworkError` → auto-restart with 5s delay
- JSON parse errors → returns empty dict (safe fallback)
- Missing images → graceful text-only fallback
- Double task completion → prevented by date check

---

*Consistency today, IIT tomorrow. 🚀*
