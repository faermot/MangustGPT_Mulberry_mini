from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.text_decorations import html_decoration
from utils.states import FirstStates, SecondStates
from utils.unpack_send_state import get_all_data
from menu.admin_menu import send_admin_menu
from menu.broadcast import send_broadcast, send_message
from keyboards import reply
from DB.database import db
import html

router = Router()


@router.callback_query(F.data == "send_broadcast")
async def process_text(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(SecondStates.text)
    await bot.send_message(
        callback.from_user.id,
        "<b>Отправьте текст:</b>\n"
    )
    await callback.answer()


@router.message(SecondStates.text, F.text)
async def process_button(message: Message, state: FSMContext, bot: Bot):
    html_text = html_decoration.quote(message.html_text)
    decoded_html_text = html.unescape(html_text)

    await state.update_data(text=decoded_html_text)
    await state.set_state(SecondStates.button)
    await bot.send_message(
        message.from_user.id,
        "<b>Теперь отправьте название кнопки и ссылку через запятую:</b>\n"
        "(Пример: Перейти, https://example.com или нажмите 'Без кнопки')",
        reply_markup=reply.without_button
    )


@router.message(SecondStates.button, F.text)
async def process_media(message: Message, state: FSMContext, bot: Bot):
    text = message.text.strip()

    # Проверка варианта "Без кнопки"
    if text.lower() == "без кнопки":
        await state.update_data(button=None)
        await state.set_state(SecondStates.media)
        await bot.send_message(
            message.from_user.id,
            "<b>Теперь отправьте медиа:</b>\n"
            "(Фото, видео или гиф. Или нажмите кнопку 'Без медиа'.)",
            reply_markup=reply.without_media
        )
        return

    # Проверка формата "Название, ссылка"
    parts = [p.strip() for p in text.split(",", maxsplit=1)]
    if len(parts) != 2 or not parts[1].startswith(("http://", "https://")):
        await message.answer(
            "Неверный формат!\n"
            "Отправьте в формате:\n<b>Название кнопки, https://example.com</b>\n"
            "Или нажмите 'Без кнопки'."
        )
        return

    button_name, button_url = parts
    await state.update_data(button=(button_name, button_url))
    await state.set_state(SecondStates.media)

    await bot.send_message(
        message.from_user.id,
        "<b>Теперь отправьте медиа:</b>\n"
        "(Фото, видео или гиф. Или нажмите кнопку 'Без медиа'.)",
        reply_markup=reply.without_media
    )


@router.message(SecondStates.media)
async def with_media(message: Message, state: FSMContext, bot: Bot):
    media_file_id = None
    media_type = None

    if message.photo:
        media_file_id = message.photo[-1].file_id
        media_type = "photo"
    elif message.video:
        media_file_id = message.video.file_id
        media_type = "video"
    elif message.animation:
        media_file_id = message.animation.file_id
        media_type = "animation"
    elif message.text and message.text.lower() == "без медиа":
        media_file_id = None
        media_type = None
    else:
        await message.answer("Пожалуйста, отправьте корректный медиафайл или нажмите 'Без медиа'.")
        return

    await state.update_data(media=media_file_id, media_type=media_type)

    text, button, media_type, media = await get_all_data(state)

    await send_message(message.from_user.id, text, button, media_type, media, bot)
    await bot.send_message(
        message.from_user.id,
        "<b>Отправить рассылку? (Да/Нет)</b>",
        reply_markup=reply.broadcast_choice
    )
    await state.set_state(SecondStates.confirm_send)


@router.message(SecondStates.confirm_send, F.text)
async def confirm_send(message: Message, state: FSMContext, bot: Bot):
    choice = message.text.lower()
    if choice == 'да':
        await message.answer("📩 Рассылка отправлена.", reply_markup=reply.rmk)

        text, button, media_type, media = await get_all_data(state)
        await send_broadcast(message.from_user.id, text, button, media_type, media, bot)
        await send_admin_menu(bot, message)
        await state.clear()

    elif choice == 'нет':
        await message.answer("❌ Рассылка отменена.")
        await send_admin_menu(bot, message)
        await state.clear()

    else:
        await message.answer("Пожалуйста, отправьте 'Да' или 'Нет'.")


@router.callback_query(F.data == "statistics")
async def view_statistics(callback: CallbackQuery, bot: Bot):
    users_count = await db.view_users()
    unique_users_count = users_count
    await bot.send_message(callback.from_user.id, f"<b>ℹ️ Количество пользователей:</b> {unique_users_count}")
    await callback.answer()
