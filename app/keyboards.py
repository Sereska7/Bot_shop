from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data_base.requests import get_categories, get_category_items


key_main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Каталог")],
                                         [KeyboardButton(text="Корзина")],
                                         [KeyboardButton(text="О нас"),
                                          KeyboardButton(text="Контакты")]],
                               resize_keyboard=True,
                               input_field_placeholder='Выберите пункт меню...')


async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name,
                                          callback_data=f"category_{category.id}"))
    return keyboard.adjust(2).as_markup()


async def items(category_id):
    all_items = await get_category_items(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name,
                                          callback_data=f"item_{item.id}"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="backward"))
    return keyboard.adjust(2).as_markup()


async def to_back():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="ago_item"))
    keyboard.add(InlineKeyboardButton(text="В корзину", callback_data="to_basket"))
    keyboard.add(InlineKeyboardButton(text="На главную", callback_data="back_main"))
    return keyboard.adjust(2).as_markup()


async def button_del_card(card_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Удалить", callback_data=f"del_card_{card_id}"))
    return keyboard.adjust(2).as_markup()
