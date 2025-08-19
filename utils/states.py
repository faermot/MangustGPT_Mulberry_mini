from aiogram.fsm.state import StatesGroup, State


class FirstStates(StatesGroup):
    text = State()
    photo = State()


class SecondStates(StatesGroup):
    text = State()
    button = State()
    media_type = State()
    media = State()
    confirm_send = State()


class ClearHistory(StatesGroup):
    choice = State()


class ChatStates(StatesGroup):
    waiting_for_answer = State()
