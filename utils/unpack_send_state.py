from aiogram.fsm.context import FSMContext


async def get_all_data(state: FSMContext):
    data = await state.get_data()

    text_data = data.get("text")
    button_data = data.get("button")
    media_type_data = data.get("media_type")
    media_data = data.get("media")

    if isinstance(button_data, tuple):
        button_data = f"{button_data[0]},{button_data[1]}"

    return text_data, button_data, media_type_data, media_data
