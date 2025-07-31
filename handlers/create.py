from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from keyboards import get_back_menu, get_main_menu, get_processing_menu, get_result_menu
from models.states import EditStates
from services.ai_service import GeminiService
from config import MAX_MESSAGE_LENGTH
from services.language_service import LanguageService
import logging

router = Router()
gemini_service = GeminiService()
language_service = LanguageService()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "create")
async def create_post_selected(callback: CallbackQuery, state: FSMContext):
    """Обработчик выбора создания поста"""
    user_id = callback.from_user.id
    await state.update_data(task_type="create")
    await state.set_state(EditStates.waiting_for_topic)

    create_text = language_service.get_text(user_id, "task_create")

    await callback.message.edit_text(
        create_text, reply_markup=get_back_menu(user_id), parse_mode="HTML"
    )
    await callback.answer()


@router.message(EditStates.waiting_for_topic)
async def process_topic(message: Message, state: FSMContext):
    """Обработка темы для создания поста"""
    user_id = message.from_user.id

    if not message.text:
        error_text = language_service.get_text(user_id, "error_text_only")
        await message.answer(error_text)
        return

    if len(message.text) > 500:
        error_text = language_service.get_text(
            user_id, "error_topic_too_long", len(message.text)
        )
        await message.answer(error_text)
        return

    processing_text = language_service.get_text(user_id, "creating_post")
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
            "create",
            user_id,
            language_code=language_service.get_user_language(user_id),
        )

        try:
            await processing_msg.delete()
        except:
            pass

        result_prefix = language_service.get_text(user_id, "result_created")
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
            original_text=message.text, processed_text=result, task_type="create"
        )

        what_next = language_service.get_text(user_id, "what_next")
        await message.answer(what_next, reply_markup=get_result_menu(user_id))

    except Exception as e:
        logger.error(f"Ошибка при создании поста: {e}")

        try:
            await processing_msg.delete()
        except:
            pass

        error_text = language_service.get_text(user_id, "error_creating")
        await message.answer(
            error_text,
            parse_mode="HTML",
            reply_markup=get_main_menu(user_id),
        )
