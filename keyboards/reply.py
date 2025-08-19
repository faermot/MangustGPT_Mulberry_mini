from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)

without_photo = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Без фото")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Отправьте фото или нажмите кнопку ниже.",
    selective=True
)

without_media = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Без медиа")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Отправьте медиа или нажмите кнопку ниже.",
    selective=True
)

without_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Без кнопки")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)

broadcast_choice = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да"),
            KeyboardButton(text="Нет")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)

clear_history_choice = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да"),
            KeyboardButton(text="Нет")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)


rmk = ReplyKeyboardRemove()
