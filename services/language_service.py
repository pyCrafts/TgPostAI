import json
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class LanguageService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LanguageService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return

        self.storage_file = "user_languages.json"
        self.data = self._load_data()
        self.translations = self._load_translations()
        self._initialized = True

    def _load_data(self) -> Dict[str, Any]:
        """Загружает данные о языках пользователей из файла"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Ошибка загрузки языковых данных: {e}")

        return {"users": {}}

    def _save_data(self):
        """Сохраняет данные о языках пользователей в файл"""
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            logger.error(f"Ошибка сохранения языковых данных: {e}")

    def _load_translations(self) -> Dict[str, Dict[str, str]]:
        """Загружает переводы для всех языков"""
        return {
            "ru": {
                # Главное меню
                "welcome_title": "🤖 <b>AI-редактор Telegram-постов</b>",
                "welcome_text": """Привет! Я помогу тебе улучшить твои посты для Telegram с помощью искусственного интеллекта.

<b>Что я умею:</b>
✨ Улучшать структуру и читаемость постов
🔧 Исправлять грамматические и орфографические ошибки  
🎯 Делать контент более вовлекающим
📊 Анализировать посты и давать рекомендации
✂️ Сокращать или расширять тексты
📢 Публиковать готовые посты в каналы и группы

<b>Как пользоваться:</b>
1. Выбери нужную функцию в меню
2. Отправь мне свой текст
3. Получи улучшенную версию!
4. Опубликуй результат в свой канал одной кнопкой

Выбери действие:""",
                "main_menu_title": "🤖 <b>AI-редактор Telegram-постов</b>\n\nВыбери действие для работы с твоим контентом:",
                # Кнопки главного меню
                "btn_create": "✍️ Создать пост",
                "btn_improve": "✨ Улучшить пост",
                "btn_fix_errors": "🔧 Исправить ошибки",
                "btn_make_engaging": "🎯 Сделать вовлекающим",
                "btn_shorten": "✂️ Сократить",
                "btn_expand": "📝 Расширить",
                "btn_analyze": "📊 Анализ поста",
                "btn_help": "❓ Помощь",
                "btn_stats": "📊 Статистика",
                "btn_back": "🔙 Главное меню",
                "btn_language": "🌐 Язык",
                # Выбор языка
                "language_selection": "🌐 <b>Выбор языка / Language Selection</b>\n\nВыберите язык интерфейса:\nChoose interface language:",
                "btn_russian": "🇷🇺 Русский",
                "btn_english": "🇺🇸 English",
                "language_changed": "✅ Язык изменен на русский",
                # Описания задач
                "task_create": '✍️ <b>Создание поста</b>\n\nОпишите тему или идею для поста. Например:\n• "Польза утренней зарядки"\n• "Как выбрать хороший кофе"\n• "Тренды в веб-дизайне 2024"\n• "Рецепт домашней пиццы"\n\nЯ создам готовый пост с заголовком, структурированным текстом и призывом к действию.\n\n<i>Опишите тему одним сообщением</i>',
                "task_improve": "✨ <b>Улучшение поста</b>\n\nОтправь мне текст, который нужно улучшить. Я исправлю ошибки, улучшу структуру и добавлю эмодзи.",
                "task_fix_errors": "🔧 <b>Исправление ошибок</b>\n\nОтправь текст для корректуры. Я исправлю все грамматические и орфографические ошибки.",
                "task_make_engaging": "🎯 <b>Повышение вовлеченности</b>\n\nОтправь пост, который нужно сделать более вовлекающим. Я добавлю призывы к действию и эмоциональность.",
                "task_analyze": "📊 <b>Анализ поста</b>\n\nОтправь пост для анализа. Я дам подробные рекомендации по улучшению.",
                "task_shorten": "✂️ <b>Сокращение текста</b>\n\nОтправь текст, который нужно сократить. Я уберу лишнее, сохранив главную мысль.",
                "task_expand": "📝 <b>Расширение текста</b>\n\nОтправь текст для расширения. Я добавлю полезные детали и примеры.",
                # Обработка
                "processing": "🔄 <b>Обрабатываю ваш текст...</b>\n\nЭто может занять несколько секунд. Пожалуйста, подождите.",
                "creating_post": "✍️ <b>Создаю пост на заданную тему...</b>\n\nЭто может занять несколько секунд. Пожалуйста, подождите.",
                "btn_cancel": "⏹ Отменить",
                # Результаты
                "result_processing": "✅ <b>Результат обработки:</b>\n\n",
                "result_analysis": "📊 <b>Анализ вашего поста:</b>\n\n",
                "result_created": "✍️ <b>Ваш новый пост готов:</b>\n\n",
                "what_next": "Что делаем дальше?",
                "process_another": "Хотите обработать еще один текст?",
                # Кнопки результата
                "btn_edit_result": "✏️ Редактировать результат",
                "btn_publish": "📢 Опубликовать",
                "btn_process_again": "🔄 Обработать ещё",
                # Ошибки
                "error_text_only": "❌ Пожалуйста, отправьте текстовое сообщение.",
                "error_text_too_long": "❌ Текст слишком длинный! Максимальная длина: {} символов.\nВаш текст: {} символов.",
                "error_topic_too_long": "❌ Описание темы слишком длинное! Максимум 500 символов.\nВаше описание: {} символов.",
                "error_processing": "❌ <b>Произошла ошибка при обработке</b>\n\nПопробуйте еще раз или обратитесь к администратору.",
                "error_creating": "❌ <b>Произошла ошибка при создании поста</b>\n\nПопробуйте еще раз или обратитесь к администратору.",
                "processing_cancelled": "❌ <b>Обработка отменена</b>\n\nВыберите действие:",
                "unknown_message": "🤖 Используйте меню для выбора действия или команду /start",
                # Статистика
                "stats_title": "📊 <b>Ваша статистика использования AI</b>",
                "stats_today": "<b>Сегодня:</b>\n• Использовано: {}/{} запросов\n• Осталось: {} запросов",
                "stats_total": "<b>Общая статистика:</b>\n• Всего запросов: {}",
                "stats_reset": "<b>Лимит обновится:</b>\n{}",
                "stats_limit_info": "<i>Ваш дневной лимит: {} запросов к Gemini AI</i>",
                # Помощь
                "help_title": "📖 <b>Справка по использованию бота</b>",
                "help_abilities": "<b>Что я умею:</b>\n✨ Улучшать структуру и читаемость постов\n🔧 Исправлять грамматические и орфографические ошибки\n🎯 Делать контент более вовлекающим\n📊 Анализировать посты и давать рекомендации\n✂️ Сокращать или расширять тексты\n✍️ Создавать новые посты по заданной теме\n📢 Публиковать готовые посты в каналы и группы",
                "help_limits": "<b>Ограничения:</b>\n• Ваш дневной лимит: {} запросов к AI\n• Максимальная длина текста: 4096 символов\n• Лимит обновляется каждые сутки в 00:00",
                "help_usage": "<b>Как пользоваться:</b>\n1. Выберите нужную функцию в главном меню\n2. Отправьте текст или опишите тему\n3. Получите обработанный результат\n4. При желании опубликуйте в канал",
                "help_commands": "<b>Команды:</b>\n/start - главное меню\n/help - эта справка\n/stats - статистика использования AI",
                # Публикация
                "publish_start": "📢 <b>Публикация в канал/группу</b>\n\nОтправьте мне:\n• Username канала (например: @mychannel)\n• ID канала (например: -1001234567890)\n• Или перешлите любое сообщение из канала\n\n<b>Важно:</b> Бот должен быть администратором канала с правами на публикацию сообщений.\n\n<i>Для получения ID канала можете использовать @userinfobot</i>",
                "publish_checking": "🔍 Проверяю доступ к каналу...",
                "publish_error": "❌ <b>Ошибка доступа к каналу:</b>\n\n{}\n\nУбедитесь, что:\n• Бот добавлен в канал как администратор\n• У бота есть права на публикацию сообщений\n• Username или ID канала указаны правильно",
                "publish_preview": "📢 <b>Предварительный просмотр публикации</b>\n\n<b>Канал:</b> {}\n<b>Тип:</b> {}\n{}\n\n<b>Текст для публикации:</b>\n\n{}\n\nПодтвердите публикацию:",
                "publish_confirm": "✅ Опубликовать в {}",
                "publish_cancel": "❌ Отменить",
                "publish_publishing": "📤 <b>Публикую в канал {}...</b>",
                "publish_success": "✅ <b>Пост успешно опубликован!</b>\n\nКанал: {}\n{}",
                "publish_error_final": "❌ <b>Ошибка публикации</b>\n\nВозможные причины:\n• Бот потерял права администратора\n• Канал был удален или заблокирован\n• Проблемы с подключением\n\nПопробуйте еще раз или проверьте настройки канала.",
                "publish_cancelled": "❌ <b>Публикация отменена</b>\n\nВыберите действие:",
                "publish_no_text": "❌ Нет текста для публикации",
                "publish_invalid_format": "❌ Неверный формат. Используйте:\n• @username канала\n• ID канала (-1001234567890)\n• Или перешлите сообщение из канала",
                "publish_send_channel": "❌ Отправьте username канала, ID или перешлите сообщение",
                "publish_no_data": "❌ Ошибка: нет данных для публикации",
                "publish_cancelled_short": "❌ Публикация отменена",
                # Общие
                "max_length_info": "<i>Максимальная длина: {} символов</i>",
            },
            "en": {
                # Main menu
                "welcome_title": "🤖 <b>AI Telegram Post Editor</b>",
                "welcome_text": """Hello! I'll help you improve your Telegram posts using artificial intelligence.

<b>What I can do:</b>
✨ Improve post structure and readability
🔧 Fix grammatical and spelling errors
🎯 Make content more engaging
📊 Analyze posts and provide recommendations
✂️ Shorten or expand texts
📢 Publish ready posts to channels and groups

<b>How to use:</b>
1. Choose the needed function from the menu
2. Send me your text
3. Get an improved version!
4. Publish the result to your channel with one button

Choose an action:""",
                "main_menu_title": "🤖 <b>AI Telegram Post Editor</b>\n\nChoose an action to work with your content:",
                # Main menu buttons
                "btn_create": "✍️ Create Post",
                "btn_improve": "✨ Improve Post",
                "btn_fix_errors": "🔧 Fix Errors",
                "btn_make_engaging": "🎯 Make Engaging",
                "btn_shorten": "✂️ Shorten",
                "btn_expand": "📝 Expand",
                "btn_analyze": "📊 Analyze Post",
                "btn_help": "❓ Help",
                "btn_stats": "📊 Statistics",
                "btn_back": "🔙 Main Menu",
                "btn_language": "🌐 Language",
                # Language selection
                "language_selection": "🌐 <b>Language Selection / Выбор языка</b>\n\nChoose interface language:\nВыберите язык интерфейса:",
                "btn_russian": "🇷🇺 Русский",
                "btn_english": "🇺🇸 English",
                "language_changed": "✅ Language changed to English",
                # Task descriptions
                "task_create": '✍️ <b>Create Post</b>\n\nDescribe the topic or idea for the post. For example:\n• "Benefits of morning exercise"\n• "How to choose good coffee"\n• "Web design trends 2024"\n• "Homemade pizza recipe"\n\nI\'ll create a ready post with title, structured text and call to action.\n\n<i>Describe the topic in one message</i>',
                "task_improve": "✨ <b>Improve Post</b>\n\nSend me the text that needs improvement. I'll fix errors, improve structure and add emojis.",
                "task_fix_errors": "🔧 <b>Fix Errors</b>\n\nSend text for proofreading. I'll fix all grammatical and spelling errors.",
                "task_make_engaging": "🎯 <b>Make Engaging</b>\n\nSend a post that needs to be more engaging. I'll add calls to action and emotionality.",
                "task_analyze": "📊 <b>Analyze Post</b>\n\nSend a post for analysis. I'll give detailed recommendations for improvement.",
                "task_shorten": "✂️ <b>Shorten Text</b>\n\nSend text that needs to be shortened. I'll remove unnecessary parts while keeping the main idea.",
                "task_expand": "📝 <b>Expand Text</b>\n\nSend text for expansion. I'll add useful details and examples.",
                # Processing
                "processing": "🔄 <b>Processing your text...</b>\n\nThis may take a few seconds. Please wait.",
                "creating_post": "✍️ <b>Creating post on the given topic...</b>\n\nThis may take a few seconds. Please wait.",
                "btn_cancel": "⏹ Cancel",
                # Results
                "result_processing": "✅ <b>Processing result:</b>\n\n",
                "result_analysis": "📊 <b>Analysis of your post:</b>\n\n",
                "result_created": "✍️ <b>Your new post is ready:</b>\n\n",
                "what_next": "What's next?",
                "process_another": "Want to process another text?",
                # Result buttons
                "btn_edit_result": "✏️ Edit Result",
                "btn_publish": "📢 Publish",
                "btn_process_again": "🔄 Process Again",
                # Errors
                "error_text_only": "❌ Please send a text message.",
                "error_text_too_long": "❌ Text is too long! Maximum length: {} characters.\nYour text: {} characters.",
                "error_topic_too_long": "❌ Topic description is too long! Maximum 500 characters.\nYour description: {} characters.",
                "error_processing": "❌ <b>An error occurred during processing</b>\n\nTry again or contact the administrator.",
                "error_creating": "❌ <b>An error occurred while creating the post</b>\n\nTry again or contact the administrator.",
                "processing_cancelled": "❌ <b>Processing cancelled</b>\n\nChoose an action:",
                "unknown_message": "🤖 Use the menu to choose an action or /start command",
                # Statistics
                "stats_title": "📊 <b>Your AI Usage Statistics</b>",
                "stats_today": "<b>Today:</b>\n• Used: {}/{} requests\n• Remaining: {} requests",
                "stats_total": "<b>Total statistics:</b>\n• Total requests: {}",
                "stats_reset": "<b>Limit will reset:</b>\n{}",
                "stats_limit_info": "<i>Your daily limit: {} requests to Gemini AI</i>",
                # Help
                "help_title": "📖 <b>Bot Usage Guide</b>",
                "help_abilities": "<b>What I can do:</b>\n✨ Improve post structure and readability\n🔧 Fix grammatical and spelling errors\n🎯 Make content more engaging\n📊 Analyze posts and provide recommendations\n✂️ Shorten or expand texts\n✍️ Create new posts on given topics\n📢 Publish ready posts to channels and groups",
                "help_limits": "<b>Limitations:</b>\n• Your daily limit: {} AI requests\n• Maximum text length: 4096 characters\n• Limit resets every day at 00:00",
                "help_usage": "<b>How to use:</b>\n1. Choose the needed function from the main menu\n2. Send text or describe the topic\n3. Get the processed result\n4. Optionally publish to a channel",
                "help_commands": "<b>Commands:</b>\n/start - main menu\n/help - this guide\n/stats - AI usage statistics",
                # Publishing
                "publish_start": "📢 <b>Publish to Channel/Group</b>\n\nSend me:\n• Channel username (e.g., @mychannel)\n• Channel ID (e.g., -1001234567890)\n• Or forward any message from the channel\n\n<b>Important:</b> The bot must be an administrator of the channel with message posting rights.\n\n<i>To get channel ID, you can use @userinfobot</i>",
                "publish_checking": "🔍 Checking channel access...",
                "publish_error": "❌ <b>Channel access error:</b>\n\n{}\n\nMake sure that:\n• Bot is added to the channel as administrator\n• Bot has message posting rights\n• Username or channel ID is correct",
                "publish_preview": "📢 <b>Publication Preview</b>\n\n<b>Channel:</b> {}\n<b>Type:</b> {}\n{}\n\n<b>Text to publish:</b>\n\n{}\n\nConfirm publication:",
                "publish_confirm": "✅ Publish to {}",
                "publish_cancel": "❌ Cancel",
                "publish_publishing": "📤 <b>Publishing to channel {}...</b>",
                "publish_success": "✅ <b>Post published successfully!</b>\n\nChannel: {}\n{}",
                "publish_error_final": "❌ <b>Publication error</b>\n\nPossible reasons:\n• Bot lost administrator rights\n• Channel was deleted or blocked\n• Connection problems\n\nTry again or check channel settings.",
                "publish_cancelled": "❌ <b>Publication cancelled</b>\n\nChoose an action:",
                "publish_no_text": "❌ No text to publish",
                "publish_invalid_format": "❌ Invalid format. Use:\n• Channel @username\n• Channel ID (-1001234567890)\n• Or forward a message from the channel",
                "publish_send_channel": "❌ Send the channel username, ID, or forward a message",
                "publish_no_data": "❌ Error: no data to publish",
                "publish_cancelled_short": "❌ Publication cancelled",
                # Common
                "max_length_info": "<i>Maximum length: {} characters</i>",
            },
        }

    def get_user_language(self, user_id: int) -> str:
        """Получает язык пользователя"""
        user_id_str = str(user_id)
        return self.data["users"].get(user_id_str, "ru")  # По умолчанию русский

    def set_user_language(self, user_id: int, language: str):
        """Устанавливает язык пользователя"""
        user_id_str = str(user_id)
        self.data["users"][user_id_str] = language
        self._save_data()
        logger.info(f"Язык пользователя {user_id} изменен на {language}")

    def get_text(self, user_id: int, key: str, *args) -> str:
        """Получает переведенный текст для пользователя"""
        language = self.get_user_language(user_id)

        if language not in self.translations:
            language = "ru"

        text = self.translations[language].get(key, key)

        if args:
            try:
                return text.format(*args)
            except (IndexError, ValueError):
                return text

        return text

    def has_language_set(self, user_id: int) -> bool:
        """Проверяет, установлен ли язык у пользователя"""
        user_id_str = str(user_id)
        return user_id_str in self.data["users"]
