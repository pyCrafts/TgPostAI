from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from keyboards import get_main_menu, get_language_selection_menu
from services.language_service import LanguageService
from models.states import LanguageStates

router = Router()
language_service = LanguageService()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id

    if not language_service.has_language_set(user_id):
        await message.answer(
            language_service.get_text(user_id, "language_selection"),
            reply_markup=get_language_selection_menu(),
            parse_mode="HTML",
        )
        await state.set_state(LanguageStates.selecting_language)
    else:
        welcome_text = language_service.get_text(user_id, "welcome_text")
        await message.answer(
            welcome_text, reply_markup=get_main_menu(user_id), parse_mode="HTML"
        )
