from aiogram import Bot
from aiogram.types import BufferedInputFile, Message
from DF_creators.create_image import create_image_with_text
from keyboards.inline import admin_menu_buttons


async def send_admin_menu(bot: Bot, message: Message):
    image_stream = await create_image_with_text()
    photo = BufferedInputFile(image_stream, "photo.png")
    await bot.send_photo(message.from_user.id, photo=photo, reply_markup=await admin_menu_buttons())
