from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards import get_main_menu, get_result_menu, get_processing_menu
from services.ai_service import GeminiService
from services.language_service import LanguageService

router = Router()
gemini_service = GeminiService()
language_service = LanguageService()


@router.callback_query(F.data == "process_again")
async def process_again(callback: CallbackQuery, state: FSMContext):
    """Повторная обработка поста"""
    user_id = callback.from_user.id
    data = await state.get_data()
    original_text = data.get("original_text")
    task_type = data.get("task_type")

    if not original_text or not task_type:
        await callback.answer("❌ Нет исходных данных для повторной обработки")
        return

    processing_text = language_service.get_text(user_id, "processing")
    await callback.message.edit_text(
        processing_text,
        parse_mode="HTML",
        reply_markup=get_processing_menu(user_id),
    )

    try:
        new_result = await gemini_service.improve_post(
            original_text,
            task_type,
            user_id,
            language_code=language_service.get_user_language(user_id),
        )
    except Exception:
        error_text = language_service.get_text(user_id, "error_processing")
        await callback.message.edit_text(
            error_text, reply_markup=get_main_menu(user_id)
        )
        return

    await state.update_data(processed_text=new_result)

    result_prefix = language_service.get_text(user_id, "result_processing")
    await callback.message.edit_text(
        f"🔁 {result_prefix}{new_result}",
        reply_markup=get_result_menu(user_id),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "cancel")
async def cancel_processing(callback: CallbackQuery, state: FSMContext):
    """Отмена обработки"""
    user_id = callback.from_user.id
    await state.clear()

    cancelled_text = language_service.get_text(user_id, "processing_cancelled")
    await callback.message.edit_text(
        cancelled_text,
        reply_markup=get_main_menu(user_id),
        parse_mode="HTML",
    )
    await callback.answer("Обработка отменена")


@router.message()
async def unknown_message(message: Message, state: FSMContext):
    """Обработчик неизвестных сообщений"""
    user_id = message.from_user.id
    current_state = await state.get_state()

    if current_state is None:
        await message.answer(
            "🤖 Используйте меню для выбора действия или команду /start",
            reply_markup=get_main_menu(user_id),
        )
