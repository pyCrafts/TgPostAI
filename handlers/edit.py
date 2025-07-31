from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from services.ai_service import GeminiService
from models.states import EditStates, PostForm
from keyboards import (
    get_main_menu,
    get_processing_menu,
    get_result_menu,
    get_back_menu,
)
from config import MAX_MESSAGE_LENGTH
from services.language_service import LanguageService
import logging

router = Router()
logger = logging.getLogger(__name__)
gemini_service = GeminiService()
language_service = LanguageService()


@router.message(EditStates.waiting_for_text)
async def process_text(message: Message, state: FSMContext):
    """Обработка отправленного текста"""
    user_id = message.from_user.id

    if not message.text:
        error_text = language_service.get_text(user_id, "error_text_only")
        await message.answer(error_text)
        return

    if len(message.text) > MAX_MESSAGE_LENGTH:
        error_text = language_service.get_text(
            user_id, "error_text_too_long", MAX_MESSAGE_LENGTH, len(message.text)
        )
        await message.answer(error_text)
        return

    data = await state.get_data()
    task_type = data.get("task_type", "improve")

    processing_text = language_service.get_text(user_id, "processing")
    processing_msg = await message.answer(
        processing_text,
        parse_mode="HTML",
        reply_markup=get_processing_menu(user_id),
    )

    await state.set_state(EditStates.processing)
    await state.update_data(processing_msg_id=processing_msg.message_id)

    try:
        result = await gemini_service.improve_post(
            message.text,
            task_type,
            user_id,
            language_code=language_service.get_user_language(user_id),
        )

        try:
            await processing_msg.delete()
        except:
            pass

        if task_type == "analyze":
            result_prefix = language_service.get_text(user_id, "result_analysis")
        else:
            result_prefix = language_service.get_text(user_id, "result_processing")

        result_text = f"{result_prefix}{result}"

        if len(result_text) > MAX_MESSAGE_LENGTH:
            parts = [
                result_text[i : i + MAX_MESSAGE_LENGTH]
                for i in range(0, len(result_text), MAX_MESSAGE_LENGTH)
            ]

            for part in parts:
                await message.answer(part, parse_mode="HTML")
        else:
            await message.answer(result_text, parse_mode="HTML")

        await state.update_data(
            original_text=message.text, processed_text=result, task_type=task_type
        )

        if task_type != "analyze":
            what_next = language_service.get_text(user_id, "what_next")
            await message.answer(what_next, reply_markup=get_result_menu(user_id))
        else:
            process_another = language_service.get_text(user_id, "process_another")
            await message.answer(process_another, reply_markup=get_main_menu(user_id))
            await state.clear()

    except Exception as e:
        logger.error(f"Ошибка при обработке текста: {e}")

        try:
            await processing_msg.delete()
        except:
            pass

        error_text = language_service.get_text(user_id, "error_processing")
        await message.answer(
            error_text,
            parse_mode="HTML",
            reply_markup=get_main_menu(user_id),
        )


@router.callback_query(F.data == "edit_result")
async def handle_manual_edit(callback: CallbackQuery, state: FSMContext):
    """Обработка ручного редактирования поста"""
    user_id = callback.from_user.id

    edit_text = language_service.get_text(user_id, "btn_edit_result")
    max_length_info = language_service.get_text(
        user_id, "max_length_info", MAX_MESSAGE_LENGTH
    )

    await callback.message.edit_text(
        f"✍️ <b>{edit_text}:</b>\n\n{max_length_info}",
        parse_mode="HTML",
        reply_markup=get_back_menu(user_id),
    )
    await state.set_state(PostForm.manual_input)


@router.message(PostForm.manual_input)
async def receive_manual_post(message: Message, state: FSMContext):
    """Получение вручную отредактированного поста"""
    user_id = message.from_user.id
    await state.update_data(processed_text=message.text)

    await message.answer(
        f"✅ Пост получен и готов к отправке:\n\n{message.text}",
        reply_markup=get_result_menu(user_id),
    )

    await state.set_state(PostForm.confirmation)
