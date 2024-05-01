from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import app.keyboards as kb
import data_base.requests as rq

router = Router()


@router.message(CommandStart())
async def start_mess(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(text="Добро пожаловать в магазин одежды", reply_markup=kb.key_main)


@router.message(F.text == "Каталог")
async def catalog(message: Message):
    await message.answer("Выберите категорю товара",
                         reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def categories(callback: CallbackQuery):
    await callback.answer("Вы выбрали категорию")
    await callback.message.answer('Выберите товар',
                                  reply_markup=await kb.items(int(callback.data.split('_')[1])))


@router.callback_query(F.data.startswith("item_"))
async def item(callback: CallbackQuery):
    item_data = await rq.get_item(int(callback.data.split('_')[1]))
    await callback.answer('Вы выбрали товар')
    await callback.message.answer(f'Название: {item_data.name}\nОписание: {item_data.description}\nЦена: {item_data.price}₽',
                                  reply_markup=await kb.to_back())


@router.callback_query(F.data.startswith('back_main'))
async def back_to_main(callback: CallbackQuery):
    await callback.answer("Вы вернулись на главную")
    await callback.message.answer("Выберите категорию",
                                  reply_markup=await kb.categories())


@router.callback_query(F.data.startswith("backward"))
async def backward_to(callback: CallbackQuery):
    await callback.answer("Вы вернулись назад")
    await callback.message.answer("Выберите категорию",
                                  reply_markup=await kb.categories())


@router.callback_query(F.data.startswith("ago_item"))
async def ago_to_item(callback: CallbackQuery):
    pass