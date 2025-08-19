import asyncio
import aiogram
from aiogram import Bot
import aiogram.exceptions
from DB.database import db
from keyboards.inline import link_keyboard_1


async def send_broadcast(admin_id, text, button, media_type, media, bot: Bot):
    user_ids = await db.list_user_id()
    max_concurrent_requests = 30  # Максимальное количество одновременно выполняемых запросов
    delay_between_requests = 0  # Задержка между запросами

    tasks = []
    for user_id in user_ids:
        while len(asyncio.all_tasks()) > max_concurrent_requests:
            await asyncio.sleep(0.1)

        tasks.append(
            asyncio.create_task(
                send_message(user_id, text, button, media_type, media, bot)
            )
        )

        await asyncio.sleep(delay_between_requests)

    results = await asyncio.gather(*tasks)
    users_count = sum(1 for result in results if result)
    users_count_not = len(user_ids) - users_count

    await bot.send_message(
        chat_id=admin_id,
        text=f"*✅ Рассылка успешно завершена. *\n"
             f"Пользователей, получивших рассылку: {users_count} \n"
             f"Пользователей *не* получивших рассылку: {users_count_not} \n\n",
        parse_mode="Markdown")


async def send_message(user_id, text, button, media_type, media, bot: Bot):
    try:
        if media_type == "photo":
            if button != "Без кнопки":
                inline_keyboard = link_keyboard_1(button)
                await bot.send_photo(
                    chat_id=user_id,
                    photo=media,
                    caption=text,
                    reply_markup=inline_keyboard
                )
            elif button == "Без кнопки":
                await bot.send_photo(
                    chat_id=user_id,
                    photo=media,
                    caption=text
                )
        elif media_type == "video":
            if button != "Без кнопки":
                inline_keyboard = link_keyboard_1(button)
                await bot.send_video(
                    chat_id=user_id,
                    video=media,
                    caption=text,
                    reply_markup=inline_keyboard
                )
            elif button == "Без кнопки":
                await bot.send_video(
                    chat_id=user_id,
                    video=media,
                    caption=text
                )
        elif media_type == "animation":
            if button != "Без кнопки":
                inline_keyboard = link_keyboard_1(button)
                await bot.send_animation(
                    chat_id=user_id,
                    animation=media,
                    caption=text,
                    reply_markup=inline_keyboard
                )
            elif button == "Без кнопки":
                await bot.send_animation(
                    chat_id=user_id,
                    animation=media,
                    caption=text
                )
        elif media_type is None:
            if button != "Без кнопки":
                inline_keyboard = link_keyboard_1(button)
                await bot.send_message(
                    chat_id=user_id,
                    text=text,
                    reply_markup=inline_keyboard
                )
            elif button == "Без кнопки":
                await bot.send_message(
                    chat_id=user_id,
                    text=text
                )
        return True

    except aiogram.exceptions.TelegramRetryAfter:
        print(
            f"RetryAfter{user_id}")
        await asyncio.sleep(60)
        await send_message(user_id, text, button, media_type, media, bot)
    except aiogram.exceptions.TelegramNotFound as e:
        print("deleted")
        print(f"ChatNotFound{user_id}: {str(e)}")
    except aiogram.exceptions.TelegramBadRequest as e:
        print("blocked")
        print(f"BotBlocked{user_id}: {str(e)}")
    except Exception as e:
        print("else")
        print(f"other error for {user_id}: {str(e)}")

    return False
