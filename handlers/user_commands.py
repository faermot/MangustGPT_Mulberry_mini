from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, CommandObject
from filters.is_admin import IsAdmin
from config_reader import config
from DB.database import db
from menu import admin_menu
from keyboards import reply
from utils.states import ClearHistory
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(CommandStart())
async def start(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    await db.add_user(message.from_user.id)
    await bot.send_message(message.from_user.id, "Здравствуйте! Чем я могу вам помочь?", reply_markup=reply.rmk)


@router.message(Command(commands=["clear", "clear_history"]))
async def clear_history(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(ClearHistory.choice)
    await bot.send_message(
        message.from_user.id,
        "<b>Вы точно уверены, что хотите очистить историю диалога?</b>\n",
        reply_markup=reply.clear_history_choice
    )


@router.message(Command(commands=["admin"]), IsAdmin(config.admin_ids_list))
async def admin(message: Message, command: CommandObject, bot: Bot):
    await admin_menu.send_admin_menu(bot, message)


@router.message(Command(commands=["help"]))
async def reference(message: Message, bot: Bot):
    await bot.send_message(
        message.from_user.id,
        "<b>📖 Справка по боту </b>\n"
        "Версия бота: <i> MangustGPT 2.8 Mulberry Mini [8]</i>\n"
        "Генерация таблиц: <i>отсутствует</i>\n"
        "Генерация изображений: <i>отсутствует</i> \n "
        "\n"
        "<i>(Данные функции находятся в разработке)</i> \n"
        "\n"
        "<b>Команды бота:</b> \n"
        "/start - перезапуск бота \n"
        "/clear - очистка истории \n"
        "/help - данное меню \n"
        "\n"
        "<b>Технические данные:</b> \n"
        "Бот был разработан в рамках персонального проекта \n"
        "с использованием платформы aiogram и библиотеки g4f \n"
        "для обеспечения бесплатного доступа к моделям генерации текста и изображений."
    )
