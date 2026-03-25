STRINGS = {
    "welcome": {
        "en": "👋 Welcome! I'll help you manage tasks from voice messages.\n\nPlease select your language:",
        "ru": "👋 Добро пожаловать! Я помогу вам управлять задачами из голосовых сообщений.\n\nВыберите язык:",
        "uz": "👋 Xush kelibsiz! Men sizga ovozli xabarlardan vazifalarni boshqarishda yordam beraman.\n\nTilingizni tanlang:",
    },
    "lang_set": {
        "en": "Language set to English.",
        "ru": "Язык установлен: Русский.",
        "uz": "Til tanlandi: O'zbek.",
    },
    "ask_provider": {
        "en": "Choose your speech-to-text provider:",
        "ru": "Выберите провайдер распознавания речи:",
        "uz": "Nutqni matnga aylantirish provayderini tanlang:",
    },
    "ask_api_key": {
        "en": "Please send me your API key as a text message.\nIt will be stored encrypted.\n\n"
              "For OpenAI: get your key at platform.openai.com/api-keys\n"
              "For Google: send your service account JSON encoded in base64.",
        "ru": "Отправьте мне ваш API-ключ текстовым сообщением.\nОн будет храниться в зашифрованном виде.\n\n"
              "Для OpenAI: получите ключ на platform.openai.com/api-keys\n"
              "Для Google: отправьте JSON сервисного аккаунта в base64.",
        "uz": "API kalitingizni matn xabari sifatida yuboring.\nU shifrlangan holda saqlanadi.\n\n"
              "OpenAI uchun: platform.openai.com/api-keys dan kalit oling\n"
              "Google uchun: xizmat hisobi JSON ni base64 formatida yuboring.",
    },
    "key_saved": {
        "en": "✅ API key saved! You're all set.\n\nSend me a voice message to create a task.",
        "ru": "✅ API-ключ сохранён! Всё готово.\n\nОтправьте голосовое сообщение, чтобы создать задачу.",
        "uz": "✅ API kalit saqlandi! Hammasi tayyor.\n\nVazifa yaratish uchun ovozli xabar yuboring.",
    },
    "transcribing": {
        "en": "🎙 Transcribing your voice message...",
        "ru": "🎙 Расшифровываю голосовое сообщение...",
        "uz": "🎙 Ovozli xabaringiz matnga aylantirilmoqda...",
    },
    "task_created": {
        "en": "📝 Task created!\n\n\"{text}\"\n\n⏰ I'll remind you in {time}.",
        "ru": "📝 Задача создана!\n\n\"{text}\"\n\n⏰ Напомню через {time}.",
        "uz": "📝 Vazifa yaratildi!\n\n\"{text}\"\n\n⏰ {time} dan keyin eslataman.",
    },
    "reminder": {
        "en": "Reminder:",
        "ru": "Напоминание:",
        "uz": "Eslatma:",
    },
    "doing_now": {
        "en": "✅ Doing right now",
        "ru": "✅ Делаю сейчас",
        "uz": "✅ Hozir qilaman",
    },
    "remind_later": {
        "en": "🔄 Remind me later",
        "ru": "🔄 Напомнить позже",
        "uz": "🔄 Keyinroq eslating",
    },
    "after_30m": {
        "en": "⏰ After 30 minutes",
        "ru": "⏰ Через 30 минут",
        "uz": "⏰ 30 daqiqadan keyin",
    },
    "after_1h": {
        "en": "⏰ After 1 hour",
        "ru": "⏰ Через 1 час",
        "uz": "⏰ 1 soatdan keyin",
    },
    "after_2h": {
        "en": "⏰ After 2 hours",
        "ru": "⏰ Через 2 часа",
        "uz": "⏰ 2 soatdan keyin",
    },
    "doing_now_confirmed": {
        "en": "Great! Good luck with your task:",
        "ru": "Отлично! Удачи с задачей:",
        "uz": "Ajoyib! Vazifangizga omad:",
    },
    "snoozed": {
        "en": "Got it! I'll remind you again in {minutes} minutes:",
        "ru": "Понял! Напомню снова через {minutes} минут:",
        "uz": "Tushundim! {minutes} daqiqadan keyin yana eslataman:",
    },
    "1_hour": {
        "en": "1 hour",
        "ru": "1 час",
        "uz": "1 soat",
    },
    "error_no_key": {
        "en": "⚠️ You haven't set up your API key yet. Use /start to set it up.",
        "ru": "⚠️ Вы ещё не настроили API-ключ. Используйте /start для настройки.",
        "uz": "⚠️ Siz hali API kalitni sozlamagansiz. Sozlash uchun /start buyrug'ini ishlating.",
    },
    "error_transcription": {
        "en": "❌ Failed to transcribe the voice message. Please check your API key or try again.",
        "ru": "❌ Не удалось расшифровать голосовое сообщение. Проверьте API-ключ или попробуйте снова.",
        "uz": "❌ Ovozli xabarni matnga aylantirib bo'lmadi. API kalitni tekshiring yoki qayta urinib ko'ring.",
    },
    "help": {
        "en": "🤖 *Task Bot Help*\n\n"
              "Send me a voice message and I'll turn it into a task with a reminder.\n\n"
              "*Commands:*\n"
              "/start - Set up the bot\n"
              "/tasks - View your active tasks\n"
              "/settings - Change language, provider, or API key\n"
              "/help - Show this message",
        "ru": "🤖 *Помощь по боту задач*\n\n"
              "Отправьте голосовое сообщение, и я превращу его в задачу с напоминанием.\n\n"
              "*Команды:*\n"
              "/start - Настроить бота\n"
              "/tasks - Посмотреть активные задачи\n"
              "/settings - Изменить язык, провайдер или API-ключ\n"
              "/help - Показать это сообщение",
        "uz": "🤖 *Vazifa boti yordami*\n\n"
              "Ovozli xabar yuboring va men uni eslatma bilan vazifaga aylantiraman.\n\n"
              "*Buyruqlar:*\n"
              "/start - Botni sozlash\n"
              "/tasks - Faol vazifalarni ko'rish\n"
              "/settings - Til, provayder yoki API kalitni o'zgartirish\n"
              "/help - Ushbu xabarni ko'rsatish",
    },
    "no_tasks": {
        "en": "You have no active tasks. Send a voice message to create one!",
        "ru": "У вас нет активных задач. Отправьте голосовое сообщение, чтобы создать!",
        "uz": "Faol vazifalaringiz yo'q. Vazifa yaratish uchun ovozli xabar yuboring!",
    },
    "tasks_header": {
        "en": "📋 *Your tasks:*\n\n",
        "ru": "📋 *Ваши задачи:*\n\n",
        "uz": "📋 *Vazifalaringiz:*\n\n",
    },
    "settings_prompt": {
        "en": "What would you like to change?",
        "ru": "Что вы хотите изменить?",
        "uz": "Nimani o'zgartirmoqchisiz?",
    },
    "change_language": {
        "en": "🌐 Language",
        "ru": "🌐 Язык",
        "uz": "🌐 Til",
    },
    "change_provider": {
        "en": "🔧 STT Provider",
        "ru": "🔧 Провайдер STT",
        "uz": "🔧 STT provayder",
    },
    "change_api_key": {
        "en": "🔑 API Key",
        "ru": "🔑 API-ключ",
        "uz": "🔑 API kalit",
    },
    "cancelled": {
        "en": "Cancelled.",
        "ru": "Отменено.",
        "uz": "Bekor qilindi.",
    },
}


def t(key: str, lang: str = "en") -> str:
    return STRINGS.get(key, {}).get(lang, STRINGS.get(key, {}).get("en", key))
