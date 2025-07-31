import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TELEGRAM_BOT_TOKEN, DEBUG
from handlers import start, help, menu, edit, publish, create, common, stats, language
from handlers.publish import init_channel_service

log_level = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(
    level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """Главная функция запуска бота"""
    if not os.path.exists("data"):
        os.makedirs("data")
    bot = Bot(
        token=TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()

    init_channel_service(bot)

    dp.include_router(start.router)
    dp.include_router(language.router)
    dp.include_router(create.router)
    dp.include_router(stats.router)
    dp.include_router(help.router)
    dp.include_router(menu.router)
    dp.include_router(edit.router)
    dp.include_router(publish.router)
    dp.include_router(common.router)

    try:
        logger.info("🚀 Запуск AI-редактора Telegram-постов...")

        await bot.delete_webhook(drop_pending_updates=True)

        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
