# Telegram Task Bot

Open-source task management Telegram bot. Send voice or text messages — the bot creates tasks and reminds you. Multi-user, multi-language.

## Features

- 🎤 **Voice messages** — auto-transcribed with OpenAI Whisper (Uzbek, English, Russian)
- 📝 **Text messages** — create tasks instantly
- ⏰ **Smart reminders** — choose when to be reminded (5min, 30min, 1hr, 2hrs)
- 🔁 **Snooze** — postpone reminders (30min, 1hr, 2hrs)
- 🌍 **3 languages** — English, O'zbekcha, Русский
- 👥 **Multi-user** — each user brings their own OpenAI API key
- 💾 **Persistent** — reminders survive bot restarts

## How It Works

1. `/start` → pick your language
2. Bot asks for your **OpenAI API key** (stored securely, message auto-deleted)
3. Send a **voice message** or **text** → task is created
4. Pick a reminder time → bot notifies you when it's time
5. Choose **"Doing right now"** ✅ or **"Remind me later"** ⏰

## Self-Hosting

### 1. Create a Telegram bot

Talk to [@BotFather](https://t.me/BotFather) on Telegram and create a new bot. Copy the token.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure

```bash
cp .env.example .env
```

Edit `.env` and add your bot token:

```
BOT_TOKEN=your_telegram_bot_token
```

> **Note:** Users provide their own OpenAI API keys through the bot — no server-side key needed.

### 4. Run

```bash
python bot.py
```

### Deploy (run 24/7)

**Railway (recommended):**
1. Push to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Add `BOT_TOKEN` in Variables
4. Done — auto-deploys on every push

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Set up language and API key |
| `/tasks` | View active tasks |
| `/language` | Change language |
| `/settings` | Update API key |
| `/help` | Show help |

## Project Structure

```
bot.py         — Bot handlers and main loop
db.py          — SQLite database (users + tasks)
i18n.py        — Translations (EN, UZ, RU)
scheduler.py   — Reminder scheduling with persistence
transcribe.py  — OpenAI Whisper voice transcription
```

## License

MIT
