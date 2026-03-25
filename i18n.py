STRINGS = {
    "welcome": {
        "en": "👋 Welcome to Task Bot!\n\n"
              "🎤 Send a voice message or text to create a task\n"
              "📦 Include 'backlog' to save to backlog\n"
              "⏰ I'll remind you when it's time!\n\n"
              "/tasks — view tasks\n"
              "/backlog — view backlog\n"
              "/done — completed tasks\n"
              "/language — change language\n"
              "/settings — change API key\n"
              "/help — help",
        "ru": "👋 Добро пожаловать в бот задач!\n\n"
              "🎤 Отправьте голосовое или текст для создания задачи\n"
              "📦 Добавьте 'backlog' чтобы сохранить в бэклог\n"
              "⏰ Я напомню, когда придёт время!\n\n"
              "/tasks — просмотр задач\n"
              "/backlog — бэклог\n"
              "/done — выполненные\n"
              "/language — сменить язык\n"
              "/settings — изменить API ключ\n"
              "/help — помощь",
        "uz": "👋 Vazifa botiga xush kelibsiz!\n\n"
              "🎤 Vazifa yaratish uchun ovozli xabar yoki matn yuboring\n"
              "📦 Beklogga saqlash uchun 'backlog' so'zini qo'shing\n"
              "⏰ Vaqti kelganda eslataman!\n\n"
              "/tasks — vazifalar\n"
              "/backlog — beklog\n"
              "/done — bajarilganlar\n"
              "/language — tilni o'zgartirish\n"
              "/settings — API kalitni o'zgartirish\n"
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
    "ask_api_key": {
        "en": "🔑 Now send me your OpenAI API key.\n\n"
              "Get one at: platform.openai.com/api-keys\n\n"
              "I'll delete your message right after saving it for security.",
        "ru": "🔑 Теперь отправьте ваш OpenAI API ключ.\n\n"
              "Получите на: platform.openai.com/api-keys\n\n"
              "Я удалю ваше сообщение сразу после сохранения для безопасности.",
        "uz": "🔑 Endi OpenAI API kalitingizni yuboring.\n\n"
              "Bu yerdan oling: platform.openai.com/api-keys\n\n"
              "Xavfsizlik uchun xabaringizni saqlagandan keyin o'chirib tashlayman.",
    },
    "key_saved": {
        "en": "✅ API key saved! You're all set.\n\n"
              "Send me a voice message or text to create your first task!",
        "ru": "✅ API ключ сохранён! Всё готово.\n\n"
              "Отправьте голосовое или текст, чтобы создать первую задачу!",
        "uz": "✅ API kalit saqlandi! Hammasi tayyor.\n\n"
              "Birinchi vazifangizni yaratish uchun ovozli xabar yoki matn yuboring!",
    },
    "key_invalid": {
        "en": "❌ That doesn't look like an OpenAI API key. It should start with 'sk-'.\nPlease try again:",
        "ru": "❌ Это не похоже на OpenAI API ключ. Он должен начинаться с 'sk-'.\nПопробуйте ещё раз:",
        "uz": "❌ Bu OpenAI API kalitiga o'xshamaydi. U 'sk-' bilan boshlanishi kerak.\nQayta urinib ko'ring:",
    },
    "key_updated": {
        "en": "✅ API key updated!",
        "ru": "✅ API ключ обновлён!",
        "uz": "✅ API kalit yangilandi!",
    },
    "settings_prompt": {
        "en": "🔑 Send me your new OpenAI API key.\n\nI'll delete your message right after saving.",
        "ru": "🔑 Отправьте новый OpenAI API ключ.\n\nЯ удалю ваше сообщение сразу после сохранения.",
        "uz": "🔑 Yangi OpenAI API kalitingizni yuboring.\n\nSaqlagandan keyin xabaringizni o'chiraman.",
    },
    "no_api_key": {
        "en": "⚠️ You haven't set up your API key yet.\nUse /start to set it up.",
        "ru": "⚠️ Вы ещё не настроили API ключ.\nИспользуйте /start для настройки.",
        "uz": "⚠️ Siz hali API kalitni sozlamagansiz.\nSozlash uchun /start buyrug'ini ishlating.",
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
    "custom_time": {
        "en": "⌨️ Custom time",
        "ru": "⌨️ Своё время",
        "uz": "⌨️ Boshqa vaqt",
    },
    "custom_time_prompt": {
        "en": "⌨️ Type a custom time:\n\n"
              "Examples: 10m, 2h, 1h30m, 18:00, 9am, tomorrow 9am",
        "ru": "⌨️ Введите своё время:\n\n"
              "Примеры: 10m, 2h, 1h30m, 18:00, 9am, tomorrow 9am",
        "uz": "⌨️ Vaqtni kiriting:\n\n"
              "Misollar: 10m, 2h, 1h30m, 18:00, 9am, tomorrow 9am",
    },
    "invalid_time": {
        "en": "❌ Couldn't understand that time. Try: 10m, 2h, 18:00, tomorrow 9am",
        "ru": "❌ Не удалось распознать время. Попробуйте: 10m, 2h, 18:00, tomorrow 9am",
        "uz": "❌ Vaqtni tushunib bo'lmadi. Misol: 10m, 2h, 18:00, tomorrow 9am",
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
        "en": "💪 Great! Go for it! I'll check back in 15 minutes.",
        "ru": "💪 Отлично! Действуйте! Проверю через 15 минут.",
        "uz": "💪 Ajoyib! Boshlang! 15 daqiqadan keyin tekshiraman.",
    },
    "followup_check": {
        "en": "🔔 Have you completed this task?",
        "ru": "🔔 Вы выполнили эту задачу?",
        "uz": "🔔 Bu vazifani bajardingizmi?",
    },
    "complete_task": {
        "en": "✅ Complete task",
        "ru": "✅ Завершить задачу",
        "uz": "✅ Vazifani yakunlash",
    },
    "task_completed": {
        "en": "🎉 Task completed! Well done!",
        "ru": "🎉 Задача выполнена! Молодец!",
        "uz": "🎉 Vazifa bajarildi! Zo'r!",
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
    "pick_task": {
        "en": "Tap a task to manage it:",
        "ru": "Нажмите на задачу для управления:",
        "uz": "Boshqarish uchun vazifani tanlang:",
    },
    "task_detail": {
        "en": "📋 Task details",
        "ru": "📋 Детали задачи",
        "uz": "📋 Vazifa tafsilotlari",
    },
    "status_active": {
        "en": "📝 Active",
        "ru": "📝 Активная",
        "uz": "📝 Faol",
    },
    "status_pending": {
        "en": "⏳ Reminder set",
        "ru": "⏳ Напоминание установлено",
        "uz": "⏳ Eslatma belgilangan",
    },
    "status_in_progress": {
        "en": "🔄 In progress",
        "ru": "🔄 В процессе",
        "uz": "🔄 Bajarilmoqda",
    },
    "btn_edit": {
        "en": "✏️ Edit",
        "ru": "✏️ Изменить",
        "uz": "✏️ Tahrirlash",
    },
    "btn_delete": {
        "en": "🗑 Delete",
        "ru": "🗑 Удалить",
        "uz": "🗑 O'chirish",
    },
    "btn_reschedule": {
        "en": "⏰ Change reminder",
        "ru": "⏰ Изменить напоминание",
        "uz": "⏰ Eslatmani o'zgartirish",
    },
    "btn_back": {
        "en": "⬅️ Back",
        "ru": "⬅️ Назад",
        "uz": "⬅️ Orqaga",
    },
    "edit_prompt": {
        "en": "✏️ Send the new text for this task:",
        "ru": "✏️ Отправьте новый текст задачи:",
        "uz": "✏️ Vazifa uchun yangi matn yuboring:",
    },
    "task_updated": {
        "en": "✅ Task updated!",
        "ru": "✅ Задача обновлена!",
        "uz": "✅ Vazifa yangilandi!",
    },
    "confirm_delete": {
        "en": "🗑 Delete this task?",
        "ru": "🗑 Удалить эту задачу?",
        "uz": "🗑 Bu vazifani o'chirasizmi?",
    },
    "btn_yes": {
        "en": "Yes, delete",
        "ru": "Да, удалить",
        "uz": "Ha, o'chirish",
    },
    "btn_no": {
        "en": "No, keep",
        "ru": "Нет, оставить",
        "uz": "Yo'q, qoldirish",
    },
    "task_deleted": {
        "en": "🗑 Task deleted.",
        "ru": "🗑 Задача удалена.",
        "uz": "🗑 Vazifa o'chirildi.",
    },
    "error_transcription": {
        "en": "❌ Couldn't transcribe the voice. Please try again.",
        "ru": "❌ Не удалось распознать голос. Попробуйте ещё раз.",
        "uz": "❌ Ovozni aniqlab bo'lmadi. Qayta urinib ko'ring.",
    },
    # ── Backlog ──
    "backlog_added": {
        "en": "📦 Added to backlog!",
        "ru": "📦 Добавлено в бэклог!",
        "uz": "📦 Beklogga qo'shildi!",
    },
    "backlog_header": {
        "en": "📦 Your backlog:",
        "ru": "📦 Ваш бэклог:",
        "uz": "📦 Sizning beklogingiz:",
    },
    "no_backlog": {
        "en": "📦 Backlog is empty!",
        "ru": "📦 Бэклог пуст!",
        "uz": "📦 Beklog bo'sh!",
    },
    "btn_promote": {
        "en": "📋 Make active task",
        "ru": "📋 Сделать активной",
        "uz": "📋 Faol vazifaga aylantirish",
    },
    "task_promoted": {
        "en": "📋 Moved from backlog to active tasks!",
        "ru": "📋 Перемещено из бэклога в активные задачи!",
        "uz": "📋 Beklogdan faol vazifalar ro'yxatiga ko'chirildi!",
    },
    # ── Done ──
    "done_header": {
        "en": "✅ Completed tasks:",
        "ru": "✅ Выполненные задачи:",
        "uz": "✅ Bajarilgan vazifalar:",
    },
    "no_done": {
        "en": "No completed tasks yet.",
        "ru": "Пока нет выполненных задач.",
        "uz": "Hali bajarilgan vazifalar yo'q.",
    },
    "btn_reopen": {
        "en": "🔄 Reopen",
        "ru": "🔄 Открыть заново",
        "uz": "🔄 Qayta ochish",
    },
    "task_reopened": {
        "en": "🔄 Task reopened!",
        "ru": "🔄 Задача открыта заново!",
        "uz": "🔄 Vazifa qayta ochildi!",
    },
    # ── Daily Report ──
    "daily_report": {
        "en": "☀️ Good morning! Here's your daily report:",
        "ru": "☀️ Доброе утро! Ваш ежедневный отчёт:",
        "uz": "☀️ Xayrli tong! Kunlik hisobotingiz:",
    },
    "report_active": {
        "en": "📋 Active tasks",
        "ru": "📋 Активные задачи",
        "uz": "📋 Faol vazifalar",
    },
    "report_backlog": {
        "en": "📦 Backlog items",
        "ru": "📦 Бэклог",
        "uz": "📦 Beklog",
    },
    "report_empty": {
        "en": "☀️ Good morning! No tasks or backlog items. Enjoy your day!",
        "ru": "☀️ Доброе утро! Нет задач или бэклога. Хорошего дня!",
        "uz": "☀️ Xayrli tong! Vazifalar va beklog bo'sh. Yaxshi kun tilayman!",
    },
    "help": {
        "en": "🤖 Task Bot Help\n\n"
              "🎤 Send a voice message — I'll transcribe and create a task\n"
              "📝 Or just type your task as text\n"
              "📦 Include 'backlog' to save to backlog instead\n"
              "⏰ Pick when to be reminded (presets or custom time)\n"
              "✅ Mark done or snooze when reminded\n\n"
              "Commands:\n"
              "/tasks — view & manage active tasks\n"
              "/backlog — view backlog items\n"
              "/done — view completed tasks\n"
              "/language — change language\n"
              "/settings — change API key\n"
              "/help — this message\n\n"
              "📋 Daily report sent every morning at 9:00",
        "ru": "🤖 Помощь по боту\n\n"
              "🎤 Отправьте голосовое — распознаю и создам задачу\n"
              "📝 Или просто напишите текстом\n"
              "📦 Добавьте 'backlog' для сохранения в бэклог\n"
              "⏰ Выберите время (готовые или своё)\n"
              "✅ Отметьте или отложите при напоминании\n\n"
              "Команды:\n"
              "/tasks — просмотр и управление задачами\n"
              "/backlog — бэклог\n"
              "/done — выполненные задачи\n"
              "/language — сменить язык\n"
              "/settings — изменить API ключ\n"
              "/help — эта справка\n\n"
              "📋 Ежедневный отчёт каждое утро в 9:00",
        "uz": "🤖 Bot yordami\n\n"
              "🎤 Ovozli xabar yuboring — matnga aylantirib vazifa yarataman\n"
              "📝 Yoki shunchaki matn yozing\n"
              "📦 Beklogga saqlash uchun 'backlog' so'zini qo'shing\n"
              "⏰ Eslatma vaqtini tanlang (tayyor yoki boshqa)\n"
              "✅ Eslatganimda bajarildi deb belgilang yoki keyinga qoldiring\n\n"
              "Buyruqlar:\n"
              "/tasks — vazifalarni ko'rish va boshqarish\n"
              "/backlog — beklog\n"
              "/done — bajarilgan vazifalar\n"
              "/language — tilni o'zgartirish\n"
              "/settings — API kalitni o'zgartirish\n"
              "/help — ushbu yordam\n\n"
              "📋 Har kuni ertalab 9:00 da hisobot yuboriladi",
    },
}


def t(key: str, lang: str = "en") -> str:
    """Get translated string by key and language code."""
    return STRINGS.get(key, {}).get(lang, STRINGS.get(key, {}).get("en", key))
