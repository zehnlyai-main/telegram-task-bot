from datetime import datetime, timezone, timedelta, time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, JobQueue

from i18n import t
import db

# Tashkent timezone (UTC+5)
TZ_OFFSET = timezone(timedelta(hours=5))


def schedule_reminder(job_queue: JobQueue, task_id: int, chat_id: int,
                      task_text: str, remind_at: datetime, lang: str) -> None:
    """Schedule a one-time reminder job."""
    delay = (remind_at - datetime.now(timezone.utc)).total_seconds()
    if delay < 0:
        delay = 0

    job_name = f"reminder_{task_id}"

    # Remove existing job for this task if any
    existing = job_queue.get_jobs_by_name(job_name)
    for job in existing:
        job.schedule_removal()

    job_queue.run_once(
        callback=_reminder_callback,
        when=delay,
        chat_id=chat_id,
        name=job_name,
        data={"task_id": task_id, "text": task_text, "lang": lang},
    )


async def _reminder_callback(context: CallbackContext) -> None:
    """Send the reminder notification with action buttons."""
    data = context.job.data
    task_id = data["task_id"]
    text = data["text"]
    lang = data["lang"]

    # Verify task is still pending
    task = await db.get_task(task_id)
    if not task or task["status"] == "done":
        return

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(t("doing_now", lang), callback_data=f"done:{task_id}")],
        [InlineKeyboardButton(t("remind_later", lang), callback_data=f"later:{task_id}")],
    ])

    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text=f"{t('reminder', lang)}\n\n📋 {text}",
        reply_markup=keyboard,
    )


def schedule_followup(job_queue: JobQueue, task_id: int, chat_id: int,
                      task_text: str, lang: str, delay_minutes: int = 15) -> None:
    """Schedule a follow-up check after user says they're doing a task."""
    job_name = f"followup_{task_id}"

    # Remove existing followup for this task if any
    existing = job_queue.get_jobs_by_name(job_name)
    for job in existing:
        job.schedule_removal()

    job_queue.run_once(
        callback=_followup_callback,
        when=delay_minutes * 60,
        chat_id=chat_id,
        name=job_name,
        data={"task_id": task_id, "text": task_text, "lang": lang},
    )


async def _followup_callback(context: CallbackContext) -> None:
    """Ask user if they completed the task."""
    data = context.job.data
    task_id = data["task_id"]
    text = data["text"]
    lang = data["lang"]

    # Verify task is still active (not already completed)
    task = await db.get_task(task_id)
    if not task or task["status"] == "done":
        return

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(t("complete_task", lang), callback_data=f"complete:{task_id}")],
        [InlineKeyboardButton(t("remind_later", lang), callback_data=f"later:{task_id}")],
    ])

    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text=f"{t('followup_check', lang)}\n\n📋 {text}",
        reply_markup=keyboard,
    )


def schedule_daily_report(job_queue: JobQueue) -> None:
    """Schedule a daily report at 9:00 AM Tashkent time (UTC+5)."""
    report_time = time(hour=4, minute=0, second=0)  # 9:00 AM UTC+5 = 4:00 AM UTC
    job_queue.run_daily(
        callback=_daily_report_callback,
        time=report_time,
        name="daily_report",
    )


async def _daily_report_callback(context: CallbackContext) -> None:
    """Send daily morning report to all users."""
    users = await db.get_all_users()

    for user in users:
        user_id = user["user_id"]
        lang = user.get("language", "en")

        active = await db.get_user_tasks(user_id)
        backlog = await db.get_backlog_tasks(user_id)

        if not active and not backlog:
            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=t("report_empty", lang),
                )
            except Exception:
                pass
            continue

        lines = f"{t('daily_report', lang)}\n"

        if active:
            lines += f"\n{t('report_active', lang)} ({len(active)}):\n"
            for i, task in enumerate(active, 1):
                status_icon = {"pending": "⏳", "in_progress": "🔄"}.get(task["status"], "📝")
                lines += f"  {i}. {status_icon} {task['text']}\n"

        if backlog:
            lines += f"\n{t('report_backlog', lang)} ({len(backlog)}):\n"
            for i, task in enumerate(backlog, 1):
                lines += f"  {i}. 📦 {task['text']}\n"

        try:
            await context.bot.send_message(chat_id=user_id, text=lines)
        except Exception:
            pass  # User may have blocked the bot


async def restore_reminders(app) -> None:
    """Restore all pending reminders from database on bot startup."""
    tasks = await db.get_pending_tasks()
    for task in tasks:
        user = await db.get_user(task["user_id"])
        if not user:
            continue
        remind_at = datetime.fromisoformat(task["remind_at"])
        if remind_at.tzinfo is None:
            remind_at = remind_at.replace(tzinfo=timezone.utc)
        schedule_reminder(
            app.job_queue, task["id"], task["user_id"],
            task["text"], remind_at, user["language"],
        )
