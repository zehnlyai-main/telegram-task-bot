import os
import re
import logging
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

import db
from i18n import t
from transcribe import transcribe
from time_parser import parse_time
from scheduler import (
    schedule_reminder, schedule_followup, schedule_daily_report,
    restore_reminders,
)

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

BACKLOG_RE = re.compile(r'\bbacklog\b', re.IGNORECASE)


# ── Commands ──────────────────────────────────────────────────


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show language selection on /start."""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="lang:uz")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang:en")],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang:ru")],
    ])
    await update.message.reply_text(
        "🌍 Tilni tanlang / Choose language / Выберите язык:",
        reply_markup=keyboard,
    )


async def cmd_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Change language with /language."""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="lang:uz")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang:en")],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang:ru")],
    ])
    user = await db.get_user(update.effective_user.id)
    lang = user["language"] if user else "en"
    await update.message.reply_text(t("choose_language", lang), reply_markup=keyboard)


async def cmd_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Change API key with /settings."""
    user_id = update.effective_user.id
    user = await db.get_user(user_id)
    lang = user["language"] if user else "en"

    context.user_data["awaiting_api_key"] = True
    await update.message.reply_text(t("settings_prompt", lang))


async def cmd_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show active tasks with tappable inline buttons."""
    user_id = update.effective_user.id
    user = await db.get_user(user_id)
    lang = user["language"] if user else "en"

    tasks = await db.get_user_tasks(user_id)

    if not tasks:
        await update.message.reply_text(t("no_tasks", lang))
        return

    lines = f"📋 {t('tasks_header', lang)}\n\n"
    buttons = []
    for i, task in enumerate(tasks, 1):
        status_icon = {"pending": "⏳", "in_progress": "🔄"}.get(task["status"], "📝")
        text_preview = task["text"][:30] + ("..." if len(task["text"]) > 30 else "")
        lines += f"{i}. {status_icon} {task['text']}\n"
        buttons.append([InlineKeyboardButton(
            f"{i}. {status_icon} {text_preview}",
            callback_data=f"task:{task['id']}",
        )])

    lines += f"\n{t('pick_task', lang)}"
    await update.message.reply_text(lines, reply_markup=InlineKeyboardMarkup(buttons))


async def cmd_backlog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show backlog items with tappable inline buttons."""
    user_id = update.effective_user.id
    user = await db.get_user(user_id)
    lang = user["language"] if user else "en"

    tasks = await db.get_backlog_tasks(user_id)

    if not tasks:
        await update.message.reply_text(t("no_backlog", lang))
        return

    lines = f"{t('backlog_header', lang)}\n\n"
    buttons = []
    for i, task in enumerate(tasks, 1):
        text_preview = task["text"][:30] + ("..." if len(task["text"]) > 30 else "")
        lines += f"{i}. 📦 {task['text']}\n"
        buttons.append([InlineKeyboardButton(
            f"{i}. 📦 {text_preview}",
            callback_data=f"bltask:{task['id']}",
        )])

    lines += f"\n{t('pick_task', lang)}"
    await update.message.reply_text(lines, reply_markup=InlineKeyboardMarkup(buttons))


async def cmd_done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show completed tasks."""
    user_id = update.effective_user.id
    user = await db.get_user(user_id)
    lang = user["language"] if user else "en"

    tasks = await db.get_done_tasks(user_id)

    if not tasks:
        await update.message.reply_text(t("no_done", lang))
        return

    lines = f"{t('done_header', lang)}\n\n"
    buttons = []
    for i, task in enumerate(tasks, 1):
        text_preview = task["text"][:30] + ("..." if len(task["text"]) > 30 else "")
        lines += f"{i}. ✅ {task['text']}\n"
        buttons.append([InlineKeyboardButton(
            f"🔄 {text_preview}",
            callback_data=f"reopen:{task['id']}",
        )])

    await update.message.reply_text(lines, reply_markup=InlineKeyboardMarkup(buttons))


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show help with /help."""
    user = await db.get_user(update.effective_user.id)
    lang = user["language"] if user else "en"
    await update.message.reply_text(t("help", lang))


# ── Voice Message Handler ─────────────────────────────────────


async def on_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Transcribe voice message and create a task or backlog item."""
    user_id = update.effective_user.id
    user = await db.get_user(user_id)
    lang = user["language"] if user else "en"

    # Ensure user exists in DB
    if not user:
        await db.upsert_user(user_id, language="en")
        user = await db.get_user(user_id)

    # Check for API key
    api_key = user.get("api_key")
    if not api_key:
        await update.message.reply_text(t("no_api_key", lang))
        return

    status_msg = await update.message.reply_text(t("transcribing", lang))

    voice = update.message.voice
    tg_file = await context.bot.get_file(voice.file_id)
    file_path = f"/tmp/{voice.file_unique_id}.oga"
    await tg_file.download_to_drive(file_path)

    try:
        text = await transcribe(file_path, api_key)
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        await status_msg.edit_text(t("error_transcription", lang))
        return
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    if not text:
        await status_msg.edit_text(t("error_transcription", lang))
        return

    # Check if it should go to backlog
    if BACKLOG_RE.search(text):
        clean_text = BACKLOG_RE.sub("", text).strip()
        clean_text = re.sub(r'\s+', ' ', clean_text)  # collapse spaces
        if not clean_text:
            clean_text = text  # fallback if only "backlog" was said
        task_id = await db.create_task(user_id, clean_text, status="backlog")
        await status_msg.edit_text(
            f"{t('backlog_added', lang)}\n\n📦 {clean_text}"
        )
        return

    task_id = await db.create_task(user_id, text)

    keyboard = _remind_time_keyboard(task_id, lang)
    await status_msg.edit_text(
        f"📝 {t('task_created', lang)}\n\n"
        f"📋 {text}\n\n"
        f"⏰ {t('when_remind', lang)}",
        reply_markup=keyboard,
    )


# ── Text Message Handler ──────────────────────────────────────


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages — API key, edit, custom time, backlog, or create task."""
    user_id = update.effective_user.id
    user = await db.get_user(user_id)
    lang = user["language"] if user else "en"
    text = update.message.text.strip()

    if not text:
        return

    # ── API key input mode ──
    if context.user_data.get("awaiting_api_key"):
        if not text.startswith("sk-"):
            await update.message.reply_text(t("key_invalid", lang))
            return

        await db.upsert_user(user_id, api_key=text)

        try:
            await update.message.delete()
        except Exception:
            pass

        context.user_data["awaiting_api_key"] = False

        is_new_user = not user or not user.get("api_key")
        if is_new_user:
            await update.message.reply_text(t("key_saved", lang))
        else:
            await update.message.reply_text(t("key_updated", lang))
        return

    # ── Edit task mode ──
    if context.user_data.get("editing_task_id"):
        task_id = context.user_data.pop("editing_task_id")
        await db.update_task(task_id, text=text)
        await update.message.reply_text(
            f"{t('task_updated', lang)}\n\n📋 {text}"
        )
        return

    # ── Custom reminder time mode ──
    if context.user_data.get("custom_remind_task_id"):
        task_id = context.user_data.pop("custom_remind_task_id")
        minutes = parse_time(text)
        if minutes is None:
            await update.message.reply_text(t("invalid_time", lang))
            context.user_data["custom_remind_task_id"] = task_id  # keep mode
            return

        remind_at = datetime.now(timezone.utc) + timedelta(minutes=minutes)
        await db.update_task(task_id, status="pending", remind_at=remind_at.isoformat())

        task = await db.get_task(task_id)
        schedule_reminder(
            context.job_queue, task_id, update.effective_chat.id,
            task["text"], remind_at, lang,
        )

        time_text = _format_time(minutes, lang)
        await update.message.reply_text(
            f"✅ {t('reminder_set', lang)} {time_text} ⏰\n\n📋 {task['text']}"
        )
        return

    # ── Ensure user exists ──
    if not user:
        await db.upsert_user(user_id, language="en")

    # ── Check for backlog keyword ──
    if BACKLOG_RE.search(text):
        clean_text = BACKLOG_RE.sub("", text).strip()
        clean_text = re.sub(r'\s+', ' ', clean_text)
        if not clean_text:
            clean_text = text
        task_id = await db.create_task(user_id, clean_text, status="backlog")
        await update.message.reply_text(
            f"{t('backlog_added', lang)}\n\n📦 {clean_text}"
        )
        return

    # ── Create task from text ──
    task_id = await db.create_task(user_id, text)

    keyboard = _remind_time_keyboard(task_id, lang)
    await update.message.reply_text(
        f"📝 {t('task_created', lang)}\n\n"
        f"📋 {text}\n\n"
        f"⏰ {t('when_remind', lang)}",
        reply_markup=keyboard,
    )


# ── Callback Handler ──────────────────────────────────────────


async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle all inline keyboard button presses."""
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = update.effective_user.id

    # ── Language selection ──
    if data.startswith("lang:"):
        lang = data.split(":")[1]
        await db.upsert_user(user_id, language=lang)

        user = await db.get_user(user_id)
        if not user.get("api_key"):
            context.user_data["awaiting_api_key"] = True
            await query.edit_message_text(
                f"{t('lang_set', lang)}\n\n{t('ask_api_key', lang)}"
            )
        else:
            await query.edit_message_text(
                f"{t('lang_set', lang)}\n\n{t('welcome', lang)}"
            )
        return

    # ── Set reminder time ──
    if data.startswith("remind:"):
        parts = data.split(":")
        minutes = int(parts[1])
        task_id = int(parts[2])
        user = await db.get_user(user_id)
        lang = user["language"] if user else "en"

        remind_at = datetime.now(timezone.utc) + timedelta(minutes=minutes)
        await db.update_task(task_id, status="pending", remind_at=remind_at.isoformat())

        task = await db.get_task(task_id)
        schedule_reminder(
            context.job_queue, task_id, update.effective_chat.id,
            task["text"], remind_at, lang,
        )

        time_text = _format_time(minutes, lang)
        await query.edit_message_text(
            f"✅ {t('reminder_set', lang)} {time_text} ⏰\n\n📋 {task['text']}"
        )
        return

    # ── Custom reminder time prompt ──
    if data.startswith("custom:"):
        task_id = int(data.split(":")[1])
        user = await db.get_user(user_id)
        lang = user["language"] if user else "en"

        context.user_data["custom_remind_task_id"] = task_id
        await query.edit_message_text(t("custom_time_prompt", lang))
        return

    # ── Doing right now → schedule follow-up in 15 min ──
    if data.startswith("done:"):
        task_id = int(data.split(":")[1])
        user = await db.get_user(user_id)
        lang = user["language"] if user else "en"
        task = await db.get_task(task_id)
        if not task:
            return

        await db.update_task(task_id, status="in_progress")
        schedule_followup(
            context.job_queue, task_id, update.effective_chat.id,
            task["text"], lang,
        )
        await query.edit_message_text(
            f"{t('doing_confirmed', lang)}\n\n📋 {task['text']}"
        )
        return

    # ── Complete task ──
    if data.startswith("complete:"):
        task_id = int(data.split(":")[1])
        user = await db.get_user(user_id)
        lang = user["language"] if user else "en"
        task = await db.get_task(task_id)
        if not task:
            return

        now = datetime.now(timezone.utc).isoformat()
        await db.update_task(task_id, status="done", completed_at=now)
        await query.edit_message_text(
            f"{t('task_completed', lang)}\n\n📋 {task['text']}"
        )
        return

    # ── Remind me later → show time options ──
    if data.startswith("later:"):
        task_id = int(data.split(":")[1])
        user = await db.get_user(user_id)
        lang = user["language"] if user else "en"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(t("after_30m", lang), callback_data=f"remind:30:{task_id}")],
            [InlineKeyboardButton(t("after_1h", lang), callback_data=f"remind:60:{task_id}")],
            [InlineKeyboardButton(t("after_2h", lang), callback_data=f"remind:120:{task_id}")],
            [InlineKeyboardButton(t("custom_time", lang), callback_data=f"custom:{task_id}")],
        ])
        await query.edit_message_text(
            f"⏰ {t('when_remind', lang)}",
            reply_markup=keyboard,
        )
        return

    # ── Task detail view (from /tasks) ──
    if data.startswith("task:"):
        task_id = int(data.split(":")[1])
        user = await db.get_user(user_id)
        lang = user["language"] if user else "en"
        task = await db.get_task(task_id)
        if not task:
            return

        status_text = {
            "active": t("status_active", lang),
            "pending": t("status_pending", lang),
            "in_progress": t("status_in_progress", lang),
        }.get(task["status"], task["status"])

        text = (
            f"{t('task_detail', lang)}\n\n"
            f"📋 {task['text']}\n"
            f"📊 {status_text}"
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(t("btn_edit", lang), callback_data=f"edit:{task_id}"),
                InlineKeyboardButton(t("btn_delete", lang), callback_data=f"delete:{task_id}"),
            ],
            [
                InlineKeyboardButton(t("btn_reschedule", lang), callback_data=f"reschedule:{task_id}"),
                InlineKeyboardButton(t("complete_task", lang), callback_data=f"complete:{task_id}"),
            ],
            [InlineKeyboardButton(t("btn_back", lang), callback_data="back_tasks")],
        ])
        await query.edit_message_text(text, reply_markup=keyboard)
        return

    # ── Backlog task detail view ──
    if data.startswith("bltask:"):
        task_id = int(data.split(":")[1])
        user = await db.get_user(user_id)
        lang = user["language"] if user else "en"
        task = await db.get_task(task_id)
        if not task:
            return

        text = f"📦 {task['text']}"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(t("btn_promote", lang), callback_data=f"promote:{task_id}")],
            [
                InlineKeyboardButton(t("btn_edit", lang), callback_data=f"edit:{task_id}"),
                InlineKeyboardButton(t("btn_delete", lang), callback_data=f"delete:{task_id}"),
            ],
            [InlineKeyboardButton(t("btn_back", lang), callback_data="back_backlog")],
        ])
        await query.edit_message_text(text, reply_markup=keyboard)
        return

    # ── Promote backlog → active task ──
    if data.startswith("promote:"):
        task_id = int(data.split(":")[1])
        user = await db.get_user(user_id)
        lang = user["language"] if user else "en"
        task = await db.get_task(task_id)
        if not task:
            return

        await db.update_task(task_id, status="active")
        keyboard = _remind_time_keyboard(task_id, lang)
        await query.edit_message_text(
            f"{t('task_promoted', lang)}\n\n"
            f"📋 {task['text']}\n\n"
            f"⏰ {t('when_remind', lang)}",
            reply_markup=keyboard,
        )
        return

    # ── Edit task ──
    if data.startswith("edit:"):
        task_id = int(data.split(":")[1])
        user = await db.get_user(user_id)
        lang = user["language"] if user else "en"

        context.user_data["editing_task_id"] = task_id
        await query.edit_message_text(t("edit_prompt", lang))
        return

    # ── Delete task (confirmation) ──
    if data.startswith("delete:"):
        task_id = int(data.split(":")[1])
        user = await db.get_user(user_id)
        lang = user["language"] if user else "en"
        task = await db.get_task(task_id)
        if not task:
            return

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(t("btn_yes", lang), callback_data=f"confirm_del:{task_id}"),
                InlineKeyboardButton(t("btn_no", lang), callback_data=f"task:{task_id}"),
            ],
        ])
        await query.edit_message_text(
            f"{t('confirm_delete', lang)}\n\n📋 {task['text']}",
            reply_markup=keyboard,
        )
        return

    # ── Confirm delete ──
    if data.startswith("confirm_del:"):
        task_id = int(data.split(":")[1])
        user = await db.get_user(user_id)
        lang = user["language"] if user else "en"

        await db.delete_task(task_id)
        await query.edit_message_text(t("task_deleted", lang))
        return

    # ── Reschedule reminder ──
    if data.startswith("reschedule:"):
        task_id = int(data.split(":")[1])
        user = await db.get_user(user_id)
        lang = user["language"] if user else "en"

        keyboard = _remind_time_keyboard(task_id, lang)
        await query.edit_message_text(
            f"⏰ {t('when_remind', lang)}",
            reply_markup=keyboard,
        )
        return

    # ── Reopen completed task ──
    if data.startswith("reopen:"):
        task_id = int(data.split(":")[1])
        user = await db.get_user(user_id)
        lang = user["language"] if user else "en"
        task = await db.get_task(task_id)
        if not task:
            return

        await db.update_task(task_id, status="active", completed_at=None)
        keyboard = _remind_time_keyboard(task_id, lang)
        await query.edit_message_text(
            f"{t('task_reopened', lang)}\n\n"
            f"📋 {task['text']}\n\n"
            f"⏰ {t('when_remind', lang)}",
            reply_markup=keyboard,
        )
        return

    # ── Back to task list ──
    if data == "back_tasks":
        user = await db.get_user(user_id)
        lang = user["language"] if user else "en"
        tasks = await db.get_user_tasks(user_id)

        if not tasks:
            await query.edit_message_text(t("no_tasks", lang))
            return

        lines = f"📋 {t('tasks_header', lang)}\n\n"
        buttons = []
        for i, task in enumerate(tasks, 1):
            status_icon = {"pending": "⏳", "in_progress": "🔄"}.get(task["status"], "📝")
            text_preview = task["text"][:30] + ("..." if len(task["text"]) > 30 else "")
            lines += f"{i}. {status_icon} {task['text']}\n"
            buttons.append([InlineKeyboardButton(
                f"{i}. {status_icon} {text_preview}",
                callback_data=f"task:{task['id']}",
            )])

        lines += f"\n{t('pick_task', lang)}"
        await query.edit_message_text(lines, reply_markup=InlineKeyboardMarkup(buttons))
        return

    # ── Back to backlog list ──
    if data == "back_backlog":
        user = await db.get_user(user_id)
        lang = user["language"] if user else "en"
        tasks = await db.get_backlog_tasks(user_id)

        if not tasks:
            await query.edit_message_text(t("no_backlog", lang))
            return

        lines = f"{t('backlog_header', lang)}\n\n"
        buttons = []
        for i, task in enumerate(tasks, 1):
            text_preview = task["text"][:30] + ("..." if len(task["text"]) > 30 else "")
            lines += f"{i}. 📦 {task['text']}\n"
            buttons.append([InlineKeyboardButton(
                f"{i}. 📦 {text_preview}",
                callback_data=f"bltask:{task['id']}",
            )])

        lines += f"\n{t('pick_task', lang)}"
        await query.edit_message_text(lines, reply_markup=InlineKeyboardMarkup(buttons))
        return


# ── Helpers ────────────────────────────────────────────────────


def _remind_time_keyboard(task_id: int, lang: str) -> InlineKeyboardMarkup:
    """Build inline keyboard for reminder time selection."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(t("in_5m", lang), callback_data=f"remind:5:{task_id}"),
            InlineKeyboardButton(t("in_30m", lang), callback_data=f"remind:30:{task_id}"),
        ],
        [
            InlineKeyboardButton(t("in_1h", lang), callback_data=f"remind:60:{task_id}"),
            InlineKeyboardButton(t("in_2h", lang), callback_data=f"remind:120:{task_id}"),
        ],
        [InlineKeyboardButton(t("custom_time", lang), callback_data=f"custom:{task_id}")],
    ])


def _format_time(minutes: int, lang: str) -> str:
    """Format minutes into a human-readable time string."""
    if minutes < 60:
        return f"{minutes} {t('minutes', lang)}"
    hours = minutes // 60
    remaining = minutes % 60
    if remaining:
        return f"{hours} {t('hours', lang)} {remaining} {t('minutes', lang)}"
    return f"{hours} {t('hours', lang)}"


# ── App Init ──────────────────────────────────────────────────


async def post_init(app: Application) -> None:
    """Initialize database, restore reminders, schedule daily report."""
    await db.init_db()
    await restore_reminders(app)
    schedule_daily_report(app.job_queue)
    logger.info("Bot started. Reminders restored. Daily report scheduled.")


def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not set. Copy .env.example → .env and add your token.")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("language", cmd_language))
    app.add_handler(CommandHandler("settings", cmd_settings))
    app.add_handler(CommandHandler("tasks", cmd_tasks))
    app.add_handler(CommandHandler("backlog", cmd_backlog))
    app.add_handler(CommandHandler("done", cmd_done))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(MessageHandler(filters.VOICE, on_voice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.add_handler(CallbackQueryHandler(on_callback))

    app.post_init = post_init

    logger.info("Starting bot...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
