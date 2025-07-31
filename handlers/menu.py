from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards import get_main_menu, get_back_menu
from models.states import EditStates
from config import MAX_MESSAGE_LENGTH
from services.language_service import LanguageService

router = Router()
language_service = LanguageService()


@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await state.clear()

    main_menu_text = language_service.get_text(user_id, "main_menu_title")
    await callback.message.edit_text(
        main_menu_text,
        reply_markup=get_main_menu(user_id),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(
    F.data.in_(
        ["improve", "fix_errors", "make_engaging", "analyze", "shorten", "expand"]
    )
)
async def task_selected(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    task_type = callback.data
    await state.update_data(task_type=task_type)
    await state.set_state(EditStates.waiting_for_text)

    task_key = f"task_{task_type}"
    task_description = language_service.get_text(user_id, task_key)
    max_length_info = language_service.get_text(
        user_id, "max_length_info", MAX_MESSAGE_LENGTH
    )

    await callback.message.edit_text(
        task_description + f"\n\n{max_length_info}",
        reply_markup=get_back_menu(user_id),
        parse_mode="HTML",
    )
    await callback.answer()
