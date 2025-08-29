from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import StateFilter
from gpt4free.conversation import conversation
from aiogram.enums.parse_mode import ParseMode
from utils.markdown_conventer import convert_to_telegram_md_v2
from utils.states import ClearHistory
from keyboards import reply
from DB.database import db
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from utils.states import ChatStates
from utils.telegram_split import split_message

router = Router()


@router.message(StateFilter(None))
async def response(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(waiting_for_answer=True)

    try:
        msg = await message.answer_sticker(
            "CAACAgIAAxkBAAEIvfpkSXR0cY6-F5MakAfTp-LeCar-AgACQzAAAplZSEqbc3Vq1yevsC8E"
        )
        await bot.send_chat_action(message.from_user.id, 'typing')

        text = convert_to_telegram_md_v2(
            await conversation.get_response(user_id=message.from_user.id, user_message=message.text)
        )

        if len(text) > 4096:
            for part in split_message(text):
                await bot.send_message(message.from_user.id, part, parse_mode=ParseMode.MARKDOWN_V2)
        else:
            await message.reply(text, parse_mode=ParseMode.MARKDOWN_V2)

        await msg.delete()

    finally:
        await state.update_data(waiting_for_answer=False)
        await state.clear()


@router.message(ClearHistory.choice)
async def clear_history(message: Message, state: FSMContext, bot: Bot):
    if message.text.lower() == "да":
        await state.clear()
        await db.clear_history(user_id=message.from_user.id)
        await bot.send_message(
            message.from_user.id,
            "<b>Контекст диалога был успешно сброшен. </b>",
            reply_markup=reply.rmk
        )
    elif message.text.lower() == "нет":
        await state.clear()
        await bot.send_message(
            message.from_user.id,
            "<b>Действие было отменено. </b>",
            reply_markup=reply.rmk
        )
    else:
        await bot.send_message(
            message.from_user.id,
            "<b>Сделайте корректный выбор: Да или Нет.</b>",
            reply_markup=reply.rmk
        )
