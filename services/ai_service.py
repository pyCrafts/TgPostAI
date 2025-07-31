import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL, DAILY_REQUESTS_LIMIT
import logging
from .rate_limiter import RateLimiter

logger = logging.getLogger(__name__)


class GeminiService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GeminiService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return

        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.rate_limiter = RateLimiter(daily_limit=DAILY_REQUESTS_LIMIT)
        self._initialized = True

    async def improve_post(
        self,
        text: str,
        task_type: str = "improve",
        user_id: int = None,
        language_code: str = "ru",
    ) -> str:
        """Создает/Улучшает пост с помощью Gemini AI"""

        if user_id is None:
            return "❌ Ошибка: не указан ID пользователя"

        if not self.rate_limiter.can_make_request(user_id):
            remaining_time = self.rate_limiter.get_reset_time()
            remaining_requests = self.rate_limiter.get_remaining_requests(user_id)
            return (
                f"❌ Превышен ваш дневной лимит запросов к AI ({DAILY_REQUESTS_LIMIT} запросов в сутки).\n\n"
                f"Лимит обновится: {remaining_time.strftime('%d.%m.%Y в %H:%M')}\n\n"
                f"Осталось запросов: {remaining_requests}"
            )

        try:
            prompts_ru = {
                "improve": """Ты - профессиональный редактор контента для Telegram. 
                Улучши этот пост:
                - Исправь грамматические и орфографические ошибки
                - Улучши структуру и читаемость
                - Добавь эмодзи где уместно
                - Сохрани основную идею и тон
                - Адаптируй под формат Telegram
                
                Исходный текст:""",
                "fix_errors": """Исправь все ошибки в этом тексте:
                - Орфографические ошибки
                - Грамматические ошибки  
                - Пунктуационные ошибки
                - Стилистические неточности
                
                Текст для исправления:""",
                "make_engaging": """Сделай этот пост более вовлекающим:
                - Добавь призыв к действию
                - Используй эмодзи для привлечения внимания
                - Сделай текст более эмоциональным
                - Добавь интригу или вопросы к аудитории
                
                Исходный пост:""",
                "shorten": """Сократи этот текст, сохранив главную мысль:
                - Убери лишние слова и повторы
                - Сделай текст более лаконичным
                - Сохрани ключевую информацию
                
                Текст для сокращения:""",
                "expand": """Расширь этот текст, добавив полезные детали:
                - Добавь больше информации по теме
                - Приведи примеры или факты
                - Сделай контент более информативным
                
                Текст для расширения:""",
                "create": """Создай интересный и вовлекающий пост для Telegram на заданную тему:
                - Сделай пост информативным и полезным
                - Добавь эмодзи для привлечения внимания
                - Используй структуру с заголовком, основным текстом и призывом к действию
                - Адаптируй под формат Telegram (короткие абзацы, читаемость)
                - Добавь хештеги если уместно
                
                Тема для поста:""",
                "analyze": """Проанализируй этот Telegram-пост и дай рекомендации по улучшению:
                - Оцени читаемость и структуру
                - Предложи улучшения для вовлечения
                - Укажи на возможные ошибки
                - Дай советы по оформлению для Telegram
                
                Пост для анализа:""",
            }

            prompts_en = {
                "improve": """You are a professional content editor for Telegram.
            Improve this post:
            - Correct grammar and spelling mistakes
            - Improve structure and readability
            - Add emojis where appropriate
            - Preserve the main idea and tone
            - Adapt to Telegram format

            Original text:""",
                "fix_errors": """Correct all errors in this text:
            - Spelling errors
            - Grammar errors
            - Punctuation errors
            - Stylistic inconsistencies

            Text to correct:""",
                "make_engaging": """Make this post more engaging:
            - Add a call to action
            - Use emojis to attract attention
            - Make the text more emotional
            - Add intrigue or questions for the audience

            Original post:""",
                "shorten": """Shorten this text while keeping the main idea:
            - Remove unnecessary words and repetitions
            - Make the text more concise
            - Preserve key information

            Text to shorten:""",
                "expand": """Expand this text by adding useful details:
            - Add more information on the topic
            - Provide examples or facts
            - Make the content more informative

            Text to expand:""",
                "create": """Create an interesting and engaging Telegram post on the given topic:
            - Make the post informative and useful
            - Add emojis to attract attention
            - Use a structure with a headline, main text, and call to action
            - Adapt to Telegram format (short paragraphs, readability)
            - Add hashtags if appropriate

            Topic for the post:""",
                "analyze": """Analyze this Telegram post and provide recommendations for improvement:
            - Assess readability and structure
            - Suggest improvements for engagement
            - Point out possible mistakes
            - Give tips on formatting for Telegram

            Post for analysis:""",
            }

            prompts = prompts_ru if language_code.startswith("ru") else prompts_en

            if language_code.startswith("ru"):
                html_instructions = """
                - Не используй Markdown-заголовки (##, ###, **, * и т.д.)
                - Просто выдай обычный текст без спецформатирования
                """
            else:
                html_instructions = """
                - Do not use Markdown headers (##, ###, **, *, etc.)
                - Just provide plain text without special formatting
                """

            prompt = prompts.get(task_type, prompts["improve"])
            full_prompt = f"{prompt}\n\n{text}\n{html_instructions}"

            response = self.model.generate_content(full_prompt)

            self.rate_limiter.increment_request_count(user_id)

            if response.text:
                return response.text.strip()
            else:
                return "Извините, не удалось обработать ваш запрос. Попробуйте еще раз."

        except Exception as e:
            logger.error(f"Ошибка при обращении к Gemini API: {e}")
            return "Произошла ошибка при обработке текста. Попробуйте позже."

    def get_user_usage_stats(self, user_id: int) -> dict:
        """Возвращает статистику использования API для пользователя"""
        return self.rate_limiter.get_user_stats(user_id)

    def get_global_usage_stats(self) -> dict:
        """Возвращает глобальную статистику использования API"""
        return self.rate_limiter.get_global_stats()
