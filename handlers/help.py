from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards import get_back_menu
from services.language_service import LanguageService
from config import DAILY_REQUESTS_LIMIT

router = Router()
language_service = LanguageService()


@router.message(F.text == "/help")
async def help_handler(message: Message):
    user_id = message.from_user.id

    title = language_service.get_text(user_id, "help_title")
    abilities = language_service.get_text(user_id, "help_abilities")
    limits = language_service.get_text(user_id, "help_limits", DAILY_REQUESTS_LIMIT)
    usage = language_service.get_text(user_id, "help_usage")
    commands = language_service.get_text(user_id, "help_commands")

    help_text = f"{title}\n\n{abilities}\n\n{limits}\n\n{usage}\n\n{commands}"

    await message.answer(
        help_text, reply_markup=get_back_menu(user_id), parse_mode="HTML"
    )


@router.callback_query(F.data == "help")
async def help_callback(callback: CallbackQuery):
    await help_handler(callback.message)
    await callback.answer()
