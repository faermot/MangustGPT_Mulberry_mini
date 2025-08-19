from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from gpt4free.conversation import conversation
from aiogram.enums.parse_mode import ParseMode
from utils.markdown_conventer import convert_headings_to_bold
from utils.states import ClearHistory
from keyboards import reply
from DB.database import db

router = Router()


@router.message(F.text.lower().in_(["хай", "хелоу", "привет", "q"]))
async def greetings(message: Message):
    await message.reply("Привееет!")


@router.message(StateFilter(None))
async def response(message: Message):
    msg = await message.answer_sticker("CAACAgIAAxkBAAEIvfpkSXR0cY6-F5MakAfTp-LeCar-AgACQzAAAplZSEqbc3Vq1yevsC8E")
    text = convert_headings_to_bold(await conversation.get_response(user_id=message.from_user.id, user_message=message.text))
    await message.reply(
        text,
        parse_mode=ParseMode.MARKDOWN
    )
    await msg.delete()


@router.message(ClearHistory.choice)
async def clear_history(message: Message, state: FSMContext, bot: Bot):
    if message.text == "Да":
        await state.clear()
        await db.clear_history(user_id=message.from_user.id)
        await bot.send_message(
            message.from_user.id,
            "<b>Контекст диалога был успешно сброшен. </b>",
            reply_markup=reply.rmk
        )

    elif message.text == "Нет":
        await state.clear()
        await bot.send_message(
            message.from_user.id,
            "<b>Действие было отменено.  </b>",
            reply_markup=reply.rmk
        )

