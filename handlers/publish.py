from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from services.channel_service import ChannelService
from models.states import PublishStates
from keyboards import (
    get_main_menu,
    get_back_menu,
    get_publish_confirm_menu,
    get_publish_success_menu,
)
from services.language_service import LanguageService

router = Router()
channel_service = None
language_service = LanguageService()


def init_channel_service(bot):
    global channel_service
    channel_service = ChannelService(bot)


@router.callback_query(F.data == "publish")
async def start_publish(callback: CallbackQuery, state: FSMContext):
    """Начало процесса публикации"""
    user_id = callback.from_user.id
    data = await state.get_data()
    processed_text = data.get("processed_text")

    if not processed_text:
        await callback.answer(language_service.get_text(user_id, "publish_no_text"))
        return

    await state.set_state(PublishStates.waiting_for_channel)

    publish_text = language_service.get_text(user_id, "publish_start")

    await callback.message.edit_text(
        publish_text, reply_markup=get_back_menu(user_id), parse_mode="HTML"
    )
    await callback.answer()


@router.message(PublishStates.waiting_for_channel)
async def process_channel_input(message: Message, state: FSMContext):
    """Обработка ввода канала для публикации"""
    user_id = message.from_user.id
    channel_id = None

    if message.forward_from_chat:
        channel_id = str(message.forward_from_chat.id)
    elif message.text:
        channel_input = message.text.strip()
        if channel_input.startswith("@"):
            channel_id = channel_input
        elif channel_input.startswith("-") or channel_input.isdigit():
            channel_id = channel_input
        else:
            await message.answer(
                language_service.get_text(user_id, "publish_invalid_format")
            )
            return
    else:
        await message.answer(language_service.get_text(user_id, "publish_send_channel"))
        return

    checking_text = language_service.get_text(user_id, "publish_checking")
    checking_msg = await message.answer(checking_text)

    validation_result = await channel_service.validate_channel_access(channel_id)

    await checking_msg.delete()

    if not validation_result["valid"]:
        error_msg = validation_result["error"] or "Неизвестная ошибка"
        error_text = language_service.get_text(user_id, "publish_error", error_msg)
        await message.answer(
            error_text,
            parse_mode="HTML",
            reply_markup=get_back_menu(user_id),
        )
        return

    chat_info = validation_result["chat_info"]
    await state.update_data(channel_id=channel_id, channel_info=chat_info)

    data = await state.get_data()
    processed_text = data.get("processed_text", "")

    username_info = (
        f"<b>Username:</b> @{chat_info['username']}" if chat_info["username"] else ""
    )
    preview_text = language_service.get_text(
        user_id,
        "publish_preview",
        chat_info["title"],
        chat_info["type"],
        username_info,
        processed_text,
    )

    await state.set_state(PublishStates.confirming_publish)

    await message.answer(
        preview_text,
        reply_markup=get_publish_confirm_menu(user_id, chat_info["title"]),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "confirm_publish")
async def confirm_publish(callback: CallbackQuery, state: FSMContext):
    """Подтверждение и выполнение публикации"""
    user_id = callback.from_user.id
    data = await state.get_data()
    channel_id = data.get("channel_id")
    processed_text = data.get("processed_text")
    channel_info = data.get("channel_info", {})

    if not channel_id or not processed_text:
        await callback.answer(language_service.get_text(user_id, "publish_no_data"))
        return

    await state.set_state(PublishStates.publishing)

    publishing_text = language_service.get_text(
        user_id, "publish_publishing", channel_info.get("title", "Unknown")
    )
    publishing_msg = await callback.message.edit_text(
        publishing_text,
        parse_mode="HTML",
    )

    success = await channel_service.publish_post(channel_id, processed_text, "HTML")

    if success:
        username_info = (
            f"Username: @{channel_info['username']}"
            if channel_info.get("username")
            else ""
        )
        success_text = language_service.get_text(
            user_id,
            "publish_success",
            channel_info.get("title", "Unknown"),
            username_info,
        )
        await publishing_msg.edit_text(
            success_text,
            reply_markup=get_publish_success_menu(user_id),
            parse_mode="HTML",
        )
    else:
        error_text = language_service.get_text(user_id, "publish_error_final")
        await publishing_msg.edit_text(
            error_text,
            reply_markup=get_main_menu(user_id),
            parse_mode="HTML",
        )

    await callback.answer()
    await state.clear()


@router.callback_query(F.data == "cancel_publish")
async def cancel_publish(callback: CallbackQuery, state: FSMContext):
    """Отмена публикации"""
    user_id = callback.from_user.id
    await state.clear()

    cancelled_text = language_service.get_text(user_id, "publish_cancelled")
    await callback.message.edit_text(
        cancelled_text,
        reply_markup=get_main_menu(user_id),
        parse_mode="HTML",
    )
    await callback.answer(language_service.get_text(user_id, "publish_cancelled_short"))
