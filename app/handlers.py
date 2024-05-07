from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext


import app.keyboards as kb
import data_base.requests as rq
import app.fsm_machine as fs

router = Router()


@router.message(CommandStart())
async def start_mess(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer_photo(photo=FSInputFile(path="./Picture/photo_name.jpg"),
                               caption="<b>Добро пожаловать в магазин одежды и обуви</b> <i>S/K Shop</i>",
                               parse_mode="HTML",
                               reply_markup=kb.key_main)


@router.message(F.text == "Каталог")
async def catalog(message: Message, state: FSMContext):
    await state.set_state(fs.ItemBack.id_category)
    await message.answer_photo(photo=FSInputFile(path='./Picture/pict.jpg'),
                               caption="<i>Выберите категорю товара</i>", parse_mode="HTML",
                               reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def categories(callback: CallbackQuery, state: FSMContext):
    await state.update_data(id_category=int(callback.data.split('_')[1]))
    await state.set_state(fs.ItemBack.id_item)
    await callback.message.delete()
    await callback.answer("Вы выбрали категорию")
    await callback.message.answer(text="<i>Выберите товар</i>", parse_mode="HTML",
                                  reply_markup=await kb.items(int(callback.data.split('_')[1])))


@router.callback_query(F.data.startswith("item_"))
async def item(callback: CallbackQuery, state: FSMContext):
    await state.update_data(id_item=int(callback.data.split('_')[1]))
    item_data = await rq.get_item(int(callback.data.split('_')[1]))
    await callback.message.delete()
    picture = await rq.get_picture(item_data.id)
    await callback.answer('Вы выбрали товар')
    await callback.message.answer_photo(photo=FSInputFile(path=picture.rout_pic),
                                        caption=f'Название: {item_data.name}\n\nОписание: {item_data.description}\n\nЦена: {item_data.price}₽',
                                        reply_markup=await kb.to_back())


@router.callback_query(F.data.startswith('back_main'))
async def back_to_main(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer("Вы вернулись на главную")
    await callback.message.answer(text="<i>Выберите категорию</i>", parse_mode="HTML",
                                  reply_markup=await kb.categories())


@router.callback_query(F.data.startswith("backward"))
async def backward_to(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer("Вы вернулись назад, в категории")
    await callback.message.answer(text="<i>Выберите категорю товара</i>", parse_mode="HTML",
                                  reply_markup=await kb.categories())


@router.callback_query(F.data.startswith("ago_item"))
async def ago_to_item(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.delete()
    await callback.answer("Вы вернулись назад")
    await callback.message.answer(text="<i>Выберите товар</i>", parse_mode="HTML",
                                  reply_markup=await kb.items(data['id_category']))


@router.callback_query(F.data.startswith("to_basket"))
async def add_basket(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    item_data = await rq.get_item(int(data['id_item']))
    await rq.add_card(
        user_id=callback.from_user.id,
        item_id=data["id_item"],
        price=item_data.price
    )
    await callback.answer("Товар добавлен в корзину")


@router.message(F.text == "Корзина")
async def get_carts_screen(message: Message):
    all_cards = await rq.get_card(message.from_user.id)
    await message.answer_photo(photo=FSInputFile(path="./Picture/cards.jpg"),
                               caption="Корзина:")
    for card in all_cards:
        name_item = await rq.get_item(card.item_id)
        await message.answer(text=f'{name_item.name}\n{card.price_item}',
                             reply_markup=await kb.button_del_card(card.card_id))


@router.callback_query(F.data.startswith("del_card_"))
async def del_card(callback: CallbackQuery):
    await rq.del_card(int(callback.data.split("_")[2]))
    await callback.message.delete()
    await callback.answer("Товар удален")
