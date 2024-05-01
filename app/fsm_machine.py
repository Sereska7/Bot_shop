from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class ItemBack(StatesGroup):
    id_item = State()