# Telegram Task Management Bot

Voice-to-task bot with reminders. Send a voice message in Uzbek, English, or Russian — the bot transcribes it, creates a task, and reminds you later.

## Setup

### 1. Create a Telegram bot

Talk to [@BotFather](https://t.me/BotFather) on Telegram and create a new bot. Copy the token.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

**System requirement:** [ffmpeg](https://ffmpeg.org/) must be installed.

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set:
- `BOT_TOKEN` — your Telegram bot token from BotFather
- `ENCRYPTION_KEY` — generate one:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 4. Run

```bash
python bot.py
```

## Usage

1. `/start` — Set up language, speech provider (OpenAI or Google), and API key
2. Send a **voice message** — bot transcribes it and creates a task with a 1-hour reminder
3. When the reminder fires, choose:
   - **Doing right now** — marks the task active
   - **Remind me later** — snooze for 30min, 1hr, or 2hrs
4. `/tasks` — view active tasks
5. `/settings` — change language, provider, or API key
6. `/help` — show commands

## Supported Languages

- English
- Russian (Русский)
- Uzbek (O'zbek)

## Speech-to-Text Providers

Each user provides their own API key:

- **OpenAI Whisper** — get a key at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Google Cloud STT** — provide a base64-encoded service account JSON

## Project Structure

```
bot.py          — Entry point, all Telegram handlers
db.py           — SQLite database (users + tasks)
transcribe.py   — OpenAI Whisper + Google STT adapters
scheduler.py    — Reminder scheduling via JobQueue
crypto.py       — Fernet encryption for API keys
i18n.py         — UI strings in 3 languages
```
