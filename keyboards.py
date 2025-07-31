from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from services.language_service import LanguageService

language_service = LanguageService()


def get_language_selection_menu() -> InlineKeyboardMarkup:
    """Меню выбора языка"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
                InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en"),
            ]
        ]
    )
    return keyboard


def get_main_menu(user_id: int) -> InlineKeyboardMarkup:
    """Главное меню бота"""
    _ = lambda key: language_service.get_text(user_id, key)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("btn_create"), callback_data="create"),
                InlineKeyboardButton(text=_("btn_improve"), callback_data="improve"),
            ],
            [
                InlineKeyboardButton(
                    text=_("btn_fix_errors"), callback_data="fix_errors"
                ),
                InlineKeyboardButton(
                    text=_("btn_make_engaging"), callback_data="make_engaging"
                ),
            ],
            [
                InlineKeyboardButton(text=_("btn_shorten"), callback_data="shorten"),
                InlineKeyboardButton(text=_("btn_expand"), callback_data="expand"),
            ],
            [InlineKeyboardButton(text=_("btn_analyze"), callback_data="analyze")],
            [
                InlineKeyboardButton(text=_("btn_help"), callback_data="help"),
                InlineKeyboardButton(text=_("btn_stats"), callback_data="stats"),
            ],
            [
                InlineKeyboardButton(text=_("btn_language"), callback_data="language"),
            ],
        ]
    )
    return keyboard


def get_back_menu(user_id: int) -> InlineKeyboardMarkup:
    """Кнопка возврата в главное меню"""
    _ = lambda key: language_service.get_text(user_id, key)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("btn_back"), callback_data="main_menu")]
        ]
    )
    return keyboard


def get_processing_menu(user_id: int) -> InlineKeyboardMarkup:
    """Меню во время обработки"""
    _ = lambda key: language_service.get_text(user_id, key)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("btn_cancel"), callback_data="cancel")]
        ]
    )
    return keyboard


def get_result_menu(user_id: int) -> InlineKeyboardMarkup:
    """Меню с результатом обработки"""
    _ = lambda key: language_service.get_text(user_id, key)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_("btn_edit_result"), callback_data="edit_result"
                ),
            ],
            [
                InlineKeyboardButton(text=_("btn_publish"), callback_data="publish"),
                InlineKeyboardButton(
                    text=_("btn_process_again"), callback_data="process_again"
                ),
            ],
            [InlineKeyboardButton(text=_("btn_back"), callback_data="main_menu")],
        ]
    )
    return keyboard


def get_publish_confirm_menu(user_id: int, channel_name: str) -> InlineKeyboardMarkup:
    """Меню подтверждения публикации"""
    _ = lambda key: language_service.get_text(user_id, key)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_("publish_confirm").format(channel_name),
                    callback_data="confirm_publish",
                ),
                InlineKeyboardButton(
                    text=_("publish_cancel"), callback_data="cancel_publish"
                ),
            ],
            [InlineKeyboardButton(text=_("btn_back"), callback_data="main_menu")],
        ]
    )
    return keyboard


def get_publish_success_menu(user_id: int) -> InlineKeyboardMarkup:
    """Меню после успешной публикации"""
    _ = lambda key: language_service.get_text(user_id, key)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_("btn_process_again"), callback_data="process_again"
                )
            ]
        ]
    )
