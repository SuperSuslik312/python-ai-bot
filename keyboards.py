from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def admin_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Добавить пользователя в вайтлист", callback_data="admin_add-whitelist")],
        [InlineKeyboardButton(text="Удалить пользователя из вайтлиста", callback_data="admin_del-whitelist")],
        [InlineKeyboardButton(text="Сделать пользователя админом", callback_data="admin_add-admin")],
        [InlineKeyboardButton(text="Отобрать права админа у пользователя", callback_data="admin_del-admin")],
        [InlineKeyboardButton(text="Закрыть", callback_data="admin_cancel-panel")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def admin_keyboard_cancel():
    buttons = [
        [InlineKeyboardButton(text="Отмена", callback_data="admin_cancel")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def user_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Стереть мне память(", callback_data="user_clear")],
        [InlineKeyboardButton(text="Задать моё поведение", callback_data="user_set-prompt")],
        [InlineKeyboardButton(text="Сбросить моё поведение до заводского", callback_data='user_reset-prompt')],
        [InlineKeyboardButton(text="Закрыть", callback_data="user_cancel-panel")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def user_keyboard_foolproof_his():
    buttons = [
        [
            InlineKeyboardButton(text="Да! Иди в жопу", callback_data="user_confirm-his"),
            InlineKeyboardButton(text="Нет, прости...", callback_data="user_no-confirm-his")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def user_keyboard_foolproof_ins():
    buttons = [
        [
            InlineKeyboardButton(text="Да!", callback_data="user_confirm-ins"),
            InlineKeyboardButton(text="Нет...", callback_data="user_no-confirm-ins")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def user_keyboard_cancel():
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="user_cancel")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
