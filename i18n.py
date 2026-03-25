STRINGS = {
    "welcome": {
        "en": "👋 Welcome to Task Bot!\n\n"
              "🎤 Send a voice message or text to create a task\n"
              "⏰ I'll remind you when it's time!\n\n"
              "/tasks — view tasks\n"
              "/language — change language\n"
              "/help — help",
        "ru": "👋 Добро пожаловать в бот задач!\n\n"
              "🎤 Отправьте голосовое или текст для создания задачи\n"
              "⏰ Я напомню, когда придёт время!\n\n"
              "/tasks — просмотр задач\n"
              "/language — сменить язык\n"
              "/help — помощь",
        "uz": "👋 Vazifa botiga xush kelibsiz!\n\n"
              "🎤 Vazifa yaratish uchun ovozli xabar yoki matn yuboring\n"
              "⏰ Vaqti kelganda eslataman!\n\n"
              "/tasks — vazifalar\n"
              "/language — tilni o'zgartirish\n"
              "/help — yordam",
    },
    "choose_language": {
        "en": "🌍 Choose your language:",
        "ru": "🌍 Выберите язык:",
        "uz": "🌍 Tilni tanlang:",
    },
    "lang_set": {
        "en": "✅ Language set to English!",
        "ru": "✅ Язык установлен: Русский!",
        "uz": "✅ Til tanlandi: O'zbekcha!",
    },
    "transcribing": {
        "en": "🎙 Transcribing your voice...",
        "ru": "🎙 Распознаю голосовое...",
        "uz": "🎙 Ovoz matnga aylantirilmoqda...",
    },
    "task_created": {
        "en": "Task created!",
        "ru": "Задача создана!",
        "uz": "Vazifa yaratildi!",
    },
    "when_remind": {
        "en": "When should I remind you?",
        "ru": "Когда напомнить?",
        "uz": "Qachon eslatay?",
    },
    "in_5m": {
        "en": "5 min",
        "ru": "5 мин",
        "uz": "5 daq",
    },
    "in_30m": {
        "en": "30 min",
        "ru": "30 мин",
        "uz": "30 daq",
    },
    "in_1h": {
        "en": "1 hour",
        "ru": "1 час",
        "uz": "1 soat",
    },
    "in_2h": {
        "en": "2 hours",
        "ru": "2 часа",
        "uz": "2 soat",
    },
    "reminder_set": {
        "en": "Reminder set for",
        "ru": "Напоминание через",
        "uz": "Eslatma belgilandi:",
    },
    "reminder": {
        "en": "🔔 Reminder!",
        "ru": "🔔 Напоминание!",
        "uz": "🔔 Eslatma!",
    },
    "doing_now": {
        "en": "✅ Doing right now",
        "ru": "✅ Делаю сейчас",
        "uz": "✅ Hozir qilaman",
    },
    "remind_later": {
        "en": "⏰ Remind me later",
        "ru": "⏰ Напомнить позже",
        "uz": "⏰ Keyinroq eslating",
    },
    "after_30m": {
        "en": "After 30 minutes",
        "ru": "Через 30 минут",
        "uz": "30 daqiqadan keyin",
    },
    "after_1h": {
        "en": "After 1 hour",
        "ru": "Через 1 час",
        "uz": "1 soatdan keyin",
    },
    "after_2h": {
        "en": "After 2 hours",
        "ru": "Через 2 часа",
        "uz": "2 soatdan keyin",
    },
    "doing_confirmed": {
        "en": "💪 Great! Good luck with your task!",
        "ru": "💪 Отлично! Удачи с задачей!",
        "uz": "💪 Ajoyib! Vazifangizga omad!",
    },
    "minutes": {
        "en": "min",
        "ru": "мин",
        "uz": "daq",
    },
    "hours": {
        "en": "hour(s)",
        "ru": "час(ов)",
        "uz": "soat",
    },
    "no_tasks": {
        "en": "🎉 No active tasks! Send a voice or text to create one.",
        "ru": "🎉 Нет активных задач! Отправьте голосовое или текст.",
        "uz": "🎉 Faol vazifalar yo'q! Ovozli xabar yoki matn yuboring.",
    },
    "tasks_header": {
        "en": "Your tasks:",
        "ru": "Ваши задачи:",
        "uz": "Vazifalaringiz:",
    },
    "error_no_key": {
        "en": "⚠️ Voice transcription not configured. Add OPENAI_API_KEY to .env file.",
        "ru": "⚠️ Распознавание голоса не настроено. Добавьте OPENAI_API_KEY в .env.",
        "uz": "⚠️ Ovoz tanish sozlanmagan. .env fayliga OPENAI_API_KEY qo'shing.",
    },
    "error_transcription": {
        "en": "❌ Couldn't transcribe the voice. Please try again.",
        "ru": "❌ Не удалось распознать голос. Попробуйте ещё раз.",
        "uz": "❌ Ovozni aniqlab bo'lmadi. Qayta urinib ko'ring.",
    },
    "help": {
        "en": "🤖 Task Bot Help\n\n"
              "🎤 Send a voice message — I'll transcribe and create a task\n"
              "📝 Or just type your task as text\n"
              "⏰ Pick when to be reminded\n"
              "✅ Mark done or snooze when reminded\n\n"
              "Commands:\n"
              "/tasks — view active tasks\n"
              "/language — change language\n"
              "/help — this message",
        "ru": "🤖 Помощь по боту\n\n"
              "🎤 Отправьте голосовое — распознаю и создам задачу\n"
              "📝 Или просто напишите текстом\n"
              "⏰ Выберите время напоминания\n"
              "✅ Отметьте или отложите при напоминании\n\n"
              "Команды:\n"
              "/tasks — активные задачи\n"
              "/language — сменить язык\n"
              "/help — эта справка",
        "uz": "🤖 Bot yordami\n\n"
              "🎤 Ovozli xabar yuboring — matnga aylantirib vazifa yarataman\n"
              "📝 Yoki shunchaki matn yozing\n"
              "⏰ Eslatma vaqtini tanlang\n"
              "✅ Eslatganimda bajarildi deb belgilang yoki keyinga qoldiring\n\n"
              "Buyruqlar:\n"
              "/tasks — faol vazifalar\n"
              "/language — tilni o'zgartirish\n"
              "/help — ushbu yordam",
    },
}


def t(key: str, lang: str = "en") -> str:
    """Get translated string by key and language code."""
    return STRINGS.get(key, {}).get(lang, STRINGS.get(key, {}).get("en", key))
