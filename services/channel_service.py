import logging
from typing import Optional, Dict, Any
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

logger = logging.getLogger(__name__)


class ChannelService:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def check_bot_permissions(self, chat_id: str) -> bool:
        """Проверяет права бота в канале/группе"""
        try:

            bot_member = await self.bot.get_chat_member(chat_id, self.bot.id)

            if bot_member.status in ["administrator", "creator"]:
                return True
            elif bot_member.status == "member":
                chat = await self.bot.get_chat(chat_id)
                return chat.type != "channel"

            return False

        except (TelegramBadRequest, TelegramForbiddenError) as e:
            logger.error(f"Ошибка проверки прав в канале {chat_id}: {e}")
            return False

    async def get_chat_info(self, chat_id: str) -> Optional[Dict[str, Any]]:
        """Получает информацию о канале/группе"""
        try:

            chat = await self.bot.get_chat(chat_id)

            return {
                "id": chat.id,
                "title": chat.title,
                "username": chat.username,
                "type": chat.type,
                "description": chat.description,
            }

        except (TelegramBadRequest, TelegramForbiddenError) as e:
            logger.error(f"Ошибка получения информации о канале {chat_id}: {e}")
            return None

    async def publish_post(
        self, chat_id: str, text: str, parse_mode: str = "HTML"
    ) -> bool:
        """Публикует пост в канал/группу"""
        try:

            await self.bot.send_message(
                chat_id=chat_id, text=text, parse_mode=parse_mode
            )

            logger.info(f"Пост успешно опубликован в {chat_id}")
            return True

        except (TelegramBadRequest, TelegramForbiddenError) as e:
            logger.error(f"Ошибка публикации в канале {chat_id}: {e}")
            return False

    async def validate_channel_access(self, chat_id: str) -> Dict[str, Any]:
        """Валидирует доступ к каналу и возвращает подробную информацию"""
        result = {
            "valid": False,
            "chat_info": None,
            "bot_can_post": False,
            "error": None,
        }

        try:
            chat_info = await self.get_chat_info(chat_id)
            if not chat_info:
                result["error"] = "Канал не найден или бот не имеет доступа"
                return result

            result["chat_info"] = chat_info

            can_post = await self.check_bot_permissions(chat_id)
            result["bot_can_post"] = can_post

            if not can_post:
                result["error"] = "Бот не имеет прав для публикации в этом канале"
                return result

            result["valid"] = True
            return result

        except Exception as e:
            logger.error(f"Ошибка валидации канала {chat_id}: {e}")
            result["error"] = f"Ошибка проверки канала: {str(e)}"
            return result
