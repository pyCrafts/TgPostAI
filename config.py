import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не найден в переменных окружения")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY не найден в переменных окружения")

MAX_MESSAGE_LENGTH = 4096
GEMINI_MODEL = "gemini-2.0-flash-exp"
DAILY_REQUESTS_LIMIT = 25
