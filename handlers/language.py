from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from services.language_service import LanguageService
from keyboards import get_language_selection_menu, get_main_menu

router = Router()
language_service = LanguageService()


@router.callback_query(F.data == "language")
async def show_language_menu(callback: CallbackQuery, state: FSMContext):
    """Показывает меню выбора языка"""
    await callback.message.edit_text(
        language_service.get_text(callback.from_user.id, "language_selection"),
        reply_markup=get_language_selection_menu(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery, state: FSMContext):
    """Устанавливает выбранный язык"""
    language_code = callback.data.split("_")[1]  # lang_ru -> ru
    user_id = callback.from_user.id

    language_service.set_user_language(user_id, language_code)

    confirmation_text = language_service.get_text(user_id, "language_changed")
    await callback.answer(confirmation_text)

    main_menu_text = language_service.get_text(user_id, "main_menu_title")
    await callback.message.edit_text(
        main_menu_text,
        reply_markup=get_main_menu(user_id),
        parse_mode="HTML",
    )

    await state.clear()
