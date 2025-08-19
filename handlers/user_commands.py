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
    await bot.send_message(message.from_user.id, "Здесь будет справка...")
