# Telegram Task Bot

Personal task management bot. Send voice or text messages — the bot creates tasks and reminds you.

## Features

- 🎤 Voice messages — auto-transcribed with OpenAI Whisper (Uzbek, English, Russian)
- 📝 Text messages — create tasks instantly
- ⏰ Smart reminders — choose when to be reminded
- 🔁 Snooze — postpone reminders (30min, 1hr, 2hrs)
- 🌍 3 languages — English, O'zbekcha, Русский
- 💾 Persistent — reminders survive bot restarts

## Setup

### 1. Get API keys

- **Telegram Bot Token** — create a bot with [@BotFather](https://t.me/BotFather)
- **OpenAI API Key** — get one at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### 2. Install

```bash
pip install -r requirements.txt
```

### 3. Configure

```bash
cp .env.example .env
```

Edit `.env` and add your keys:

```
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

### 4. Run

```bash
python bot.py
```

## Usage

1. `/start` — choose your language
2. Send a **voice message** or **text** — creates a task
3. Pick reminder time (5min, 30min, 1hr, 2hrs)
4. When reminded, choose:
   - ✅ **Doing right now** — marks task done
   - ⏰ **Remind me later** — snooze 30min / 1hr / 2hrs
5. `/tasks` — view active tasks
6. `/language` — change language
7. `/help` — help

## Project Structure

```
bot.py         — Bot handlers and main loop
db.py          — SQLite database (users + tasks)
i18n.py        — Translations (EN, UZ, RU)
scheduler.py   — Reminder scheduling with persistence
transcribe.py  — OpenAI Whisper voice transcription
```
