from aiogram.fsm.state import State, StatesGroup


class ItemBack(StatesGroup):
    id_category = State()
    id_item = State()
    user_id = State()

