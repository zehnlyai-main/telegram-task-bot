from datetime import datetime, timezone

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, JobQueue

from i18n import t
import db


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
