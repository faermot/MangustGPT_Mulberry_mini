from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def admin_menu_buttons():
    admin_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Статистика", callback_data="statistics"),
            ],
            [
                InlineKeyboardButton(text="Рассылка", callback_data="send_broadcast")
            ]],
        row_width=2,
        resize_keyboard=True)
    return admin_menu

return_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='◀️ Назад', callback_data='to_return')
        ]
    ]
)


cancel_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='⛔️ Отмена', callback_data='cancel')
        ]
    ]
)


def link_keyboard_1(text_again: str | None):
    if not text_again or text_again == "Без кнопки":
        return None

    try:
        button_text, link = map(str.strip, text_again.split(',', 1))
        inline_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=button_text, url=link)]
            ]
        )
        return inline_button
    except Exception:
        return None
