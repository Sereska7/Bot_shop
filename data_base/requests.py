from data_base.base_models import async_session
from data_base.base_models import User, Category, Item, Picture, Card
from sqlalchemy import select


async def set_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))


async def get_category_items(category_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.category == category_id))


async def get_item(item_id) -> Item:
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.id == item_id))


async def get_picture(item_id):
    async with async_session() as session:
        return await session.scalar(select(Picture).where(Picture.item_id == item_id))


async def add_card(item_id: int, price: str, user_id: int):
    async with async_session() as session:
        session.add(Card(user_id=user_id, item_id=item_id, price_item=price))
        await session.commit()


async def del_card(card_id):
    async with async_session() as session:
        card = await session.scalar(select(Card).where(Card.card_id == card_id))
        await session.delete(card)
        await session.commit()


async def get_card(user_id: int):
    async with async_session() as session:
        return await session.scalars(select(Card).where(Card.user_id == user_id))
