from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards import get_back_menu
from services.ai_service import GeminiService
from services.language_service import LanguageService

router = Router()
gemini_service = GeminiService()
language_service = LanguageService()


@router.callback_query(F.data == "stats")
async def show_stats(callback: CallbackQuery):
    """Показывает статистику использования API"""
    user_id = callback.from_user.id
    stats = gemini_service.get_user_usage_stats(user_id)

    title = language_service.get_text(user_id, "stats_title")
    today_stats = language_service.get_text(
        user_id,
        "stats_today",
        stats["requests_today"],
        stats["daily_limit"],
        stats["remaining_requests"],
    )
    total_stats = language_service.get_text(
        user_id, "stats_total", stats["total_requests"]
    )
    reset_info = language_service.get_text(
        user_id, "stats_reset", stats["reset_time"].strftime("%d.%m.%Y в %H:%M")
    )
    limit_info = language_service.get_text(
        user_id, "stats_limit_info", stats["daily_limit"]
    )

    stats_text = (
        f"{title}\n\n{today_stats}\n\n{total_stats}\n\n{reset_info}\n\n{limit_info}"
    )

    await callback.message.edit_text(
        stats_text, reply_markup=get_back_menu(user_id), parse_mode="HTML"
    )
    await callback.answer()


@router.message(F.text == "/stats")
async def stats_command(message: Message):
    """Команда для просмотра статистики"""
    user_id = message.from_user.id
    stats = gemini_service.get_user_usage_stats(user_id)

    title = language_service.get_text(user_id, "stats_title")
    today_stats = language_service.get_text(
        user_id,
        "stats_today",
        stats["requests_today"],
        stats["daily_limit"],
        stats["remaining_requests"],
    )
    total_stats = language_service.get_text(
        user_id, "stats_total", stats["total_requests"]
    )
    reset_info = language_service.get_text(
        user_id, "stats_reset", stats["reset_time"].strftime("%d.%m.%Y в %H:%M")
    )
    limit_info = language_service.get_text(
        user_id, "stats_limit_info", stats["daily_limit"]
    )

    stats_text = (
        f"{title}\n\n{today_stats}\n\n{total_stats}\n\n{reset_info}\n\n{limit_info}"
    )

    await message.answer(
        stats_text, reply_markup=get_back_menu(user_id), parse_mode="HTML"
    )
