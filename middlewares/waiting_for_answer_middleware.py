from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


class WaitingForAnswerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            state: FSMContext = data['state']
            fsm_data = await state.get_data()

            if fsm_data.get("waiting_for_answer", False):
                await event.answer("⏳ Подожди, я ещё готовлю ответ на твой предыдущий вопрос.")
                return

        return await handler(event, data)
