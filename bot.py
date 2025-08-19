import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from handlers import bot_messages, user_commands
from callbacks import administration
from config_reader import config
from DB.database import db
from middlewares.waiting_for_answer_middleware import WaitingForAnswerMiddleware


async def main():
    logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.ERROR, handlers=[logging.FileHandler("bot_errors.log", mode='a')])

    await db.init()

    bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.message.middleware(WaitingForAnswerMiddleware())

    dp.include_routers(
        user_commands.router,
        bot_messages.router,
        administration.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
