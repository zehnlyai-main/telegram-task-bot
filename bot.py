import os
import logging
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

import db
import crypto
from i18n import t
from transcribe import transcribe
from scheduler import schedule_reminder, restore_reminders

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Conversation states
CHOOSE_LANGUAGE, CHOOSE_PROVIDER, ENTER_API_KEY = range(3)
# Settings states (offset to avoid collision)
SET_LANGUAGE, SET_PROVIDER, SET_API_KEY = range(10, 13)


# ── Onboarding ──────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("O'zbek 🇺🇿", callback_data="lang:uz")],
        [InlineKeyboardButton("English 🇬🇧", callback_data="lang:en")],
        [InlineKeyboardButton("Русский 🇷🇺", callback_data="lang:ru")],
    ])
    await update.message.reply_text(t("welcome", "en"), reply_markup=keyboard)
    return CHOOSE_LANGUAGE


async def on_language_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang = query.data.split(":")[1]
    context.user_data["lang"] = lang

    user_id = update.effective_user.id
    await db.upsert_user(user_id, language=lang)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("OpenAI Whisper", callback_data="provider:openai")],
        [InlineKeyboardButton("Google Cloud STT", callback_data="provider:google")],
    ])
    await query.edit_message_text(
        f"{t('lang_set', lang)}\n\n{t('ask_provider', lang)}",
        reply_markup=keyboard,
    )
    return CHOOSE_PROVIDER


async def on_provider_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    provider = query.data.split(":")[1]
    lang = context.user_data.get("lang", "en")

    user_id = update.effective_user.id
    await db.upsert_user(user_id, stt_provider=provider)

    await query.edit_message_text(t("ask_api_key", lang))
    return ENTER_API_KEY


async def on_api_key_entered(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    lang = context.user_data.get("lang", "en")
    raw_key = update.message.text.strip()

    encrypted_key = crypto.encrypt(raw_key)
    await db.upsert_user(user_id, api_key=encrypted_key)

    # Delete the message containing the API key for security
    try:
        await update.message.delete()
    except Exception:
        pass

    await update.message.reply_text(t("key_saved", lang))
    return ConversationHandler.END


async def cmd_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = await db.get_user(update.effective_user.id)
    lang = user["language"] if user else "en"
    await update.message.reply_text(t("cancelled", lang))
    return ConversationHandler.END


# ── Settings ────────────────────────────────────────────────

async def cmd_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = await db.get_user(update.effective_user.id)
    lang = user["language"] if user else "en"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(t("change_language", lang), callback_data="set:language")],
        [InlineKeyboardButton(t("change_provider", lang), callback_data="set:provider")],
        [InlineKeyboardButton(t("change_api_key", lang), callback_data="set:api_key")],
    ])
    await update.message.reply_text(t("settings_prompt", lang), reply_markup=keyboard)
    return SET_LANGUAGE


async def on_settings_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    choice = query.data.split(":")[1]
    user = await db.get_user(update.effective_user.id)
    lang = user["language"] if user else "en"

    if choice == "language":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("O'zbek 🇺🇿", callback_data="setlang:uz")],
            [InlineKeyboardButton("English 🇬🇧", callback_data="setlang:en")],
            [InlineKeyboardButton("Русский 🇷🇺", callback_data="setlang:ru")],
        ])
        await query.edit_message_text(t("welcome", lang), reply_markup=keyboard)
        return SET_LANGUAGE
    elif choice == "provider":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("OpenAI Whisper", callback_data="setprov:openai")],
            [InlineKeyboardButton("Google Cloud STT", callback_data="setprov:google")],
        ])
        await query.edit_message_text(t("ask_provider", lang), reply_markup=keyboard)
        return SET_PROVIDER
    elif choice == "api_key":
        await query.edit_message_text(t("ask_api_key", lang))
        return SET_API_KEY
    return ConversationHandler.END


async def on_set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang = query.data.split(":")[1]
    await db.upsert_user(update.effective_user.id, language=lang)
    await query.edit_message_text(t("lang_set", lang))
    return ConversationHandler.END


async def on_set_provider(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    provider = query.data.split(":")[1]
    user = await db.get_user(update.effective_user.id)
    lang = user["language"] if user else "en"
    await db.upsert_user(update.effective_user.id, stt_provider=provider)
    await query.edit_message_text(f"✅ {t('lang_set', lang)}")
    return ConversationHandler.END


async def on_set_api_key(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    user = await db.get_user(user_id)
    lang = user["language"] if user else "en"
    raw_key = update.message.text.strip()
    encrypted_key = crypto.encrypt(raw_key)
    await db.upsert_user(user_id, api_key=encrypted_key)
    try:
        await update.message.delete()
    except Exception:
        pass
    await update.message.reply_text(t("key_saved", lang))
    return ConversationHandler.END


# ── Voice Message Handler ──────────────────────────────────

async def on_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user = await db.get_user(user_id)

    if not user or not user.get("api_key"):
        lang = user["language"] if user else "en"
        await update.message.reply_text(t("error_no_key", lang))
        return

    lang = user["language"]
    status_msg = await update.message.reply_text(t("transcribing", lang))

    voice = update.message.voice
    file = await context.bot.get_file(voice.file_id)
    file_path = f"/tmp/{voice.file_unique_id}.oga"
    await file.download_to_drive(file_path)

    try:
        api_key = crypto.decrypt(user["api_key"])
        text = await transcribe(file_path, api_key, user["stt_provider"], lang)
    except Exception as e:
        logger.error(f"Transcription failed for user {user_id}: {e}")
        await status_msg.edit_text(t("error_transcription", lang))
        return
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    if not text:
        await status_msg.edit_text(t("error_transcription", lang))
        return

    remind_at = datetime.now(timezone.utc) + timedelta(hours=1)
    task_id = await db.create_task(user_id, text, remind_at.isoformat())

    schedule_reminder(context.job_queue, task_id, update.effective_chat.id, text, remind_at, lang)

    await status_msg.edit_text(
        t("task_created", lang).format(text=text, time=t("1_hour", lang))
    )


# ── Callback Query Handler (reminders) ────────────────────

async def on_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if ":" not in data:
        return

    action, task_id_str = data.split(":", 1)

    if action not in ("doing", "snooze", "snooze_30", "snooze_60", "snooze_120"):
        return

    task_id = int(task_id_str)
    task = await db.get_task(task_id)
    if not task:
        return

    user = await db.get_user(update.effective_user.id)
    lang = user["language"] if user else "en"

    if action == "doing":
        await db.update_task(task_id, status="doing")
        await query.edit_message_text(f"✅ {t('doing_now_confirmed', lang)}\n\n{task['text']}")

    elif action == "snooze":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(t("after_30m", lang), callback_data=f"snooze_30:{task_id}")],
            [InlineKeyboardButton(t("after_1h", lang), callback_data=f"snooze_60:{task_id}")],
            [InlineKeyboardButton(t("after_2h", lang), callback_data=f"snooze_120:{task_id}")],
        ])
        await query.edit_message_reply_markup(reply_markup=keyboard)

    elif action.startswith("snooze_"):
        minutes = int(action.split("_")[1])
        new_remind_at = datetime.now(timezone.utc) + timedelta(minutes=minutes)
        await db.update_task(
            task_id,
            remind_at=new_remind_at.isoformat(),
            snooze_count=task["snooze_count"] + 1,
        )
        schedule_reminder(
            context.job_queue, task_id, query.message.chat_id,
            task["text"], new_remind_at, lang,
        )
        await query.edit_message_text(
            f"⏰ {t('snoozed', lang).format(minutes=minutes)}\n\n{task['text']}"
        )


# ── /tasks Command ─────────────────────────────────────────

async def cmd_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user = await db.get_user(user_id)
    lang = user["language"] if user else "en"

    tasks = await db.get_pending_tasks()
    user_tasks = [tk for tk in tasks if tk["user_id"] == user_id]

    if not user_tasks:
        await update.message.reply_text(t("no_tasks", lang))
        return

    lines = t("tasks_header", lang)
    for i, tk in enumerate(user_tasks, 1):
        status_icon = "⏳" if tk["status"] == "pending" else "🔄"
        lines += f"{i}. {status_icon} {tk['text']}\n"

    await update.message.reply_text(lines, parse_mode="Markdown")


# ── /help Command ──────────────────────────────────────────

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = await db.get_user(update.effective_user.id)
    lang = user["language"] if user else "en"
    await update.message.reply_text(t("help", lang), parse_mode="Markdown")


# ── App Init ───────────────────────────────────────────────

async def post_init(app: Application) -> None:
    await db.init_db()
    await restore_reminders(app)
    logger.info("Bot started. Pending reminders restored.")


def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not set. Copy .env.example to .env and add your token.")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    # Onboarding conversation
    onboarding_conv = ConversationHandler(
        entry_points=[CommandHandler("start", cmd_start)],
        states={
            CHOOSE_LANGUAGE: [CallbackQueryHandler(on_language_chosen, pattern=r"^lang:")],
            CHOOSE_PROVIDER: [CallbackQueryHandler(on_provider_chosen, pattern=r"^provider:")],
            ENTER_API_KEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, on_api_key_entered)],
        },
        fallbacks=[CommandHandler("cancel", cmd_cancel)],
    )

    # Settings conversation
    settings_conv = ConversationHandler(
        entry_points=[CommandHandler("settings", cmd_settings)],
        states={
            SET_LANGUAGE: [
                CallbackQueryHandler(on_settings_choice, pattern=r"^set:"),
                CallbackQueryHandler(on_set_language, pattern=r"^setlang:"),
            ],
            SET_PROVIDER: [
                CallbackQueryHandler(on_set_provider, pattern=r"^setprov:"),
            ],
            SET_API_KEY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, on_set_api_key),
            ],
        },
        fallbacks=[CommandHandler("cancel", cmd_cancel)],
    )

    app.add_handler(onboarding_conv)
    app.add_handler(settings_conv)
    app.add_handler(CommandHandler("tasks", cmd_tasks))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(MessageHandler(filters.VOICE, on_voice_message))
    app.add_handler(CallbackQueryHandler(on_callback_query))

    app.post_init = post_init

    logger.info("Starting bot...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
