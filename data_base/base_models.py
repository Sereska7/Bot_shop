import os
from dotenv import load_dotenv

from sqlalchemy import (BigInteger, String, ForeignKey)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


load_dotenv()
engin = create_async_engine(url=os.getenv("SQL_URL"))
async_session = async_sessionmaker(engin)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class Category(Base):
    __tablename__ = "Categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

class Item(Base):
    __tablename__ = "Items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(150))
    price: Mapped[str] = mapped_column()
    category: Mapped[int] = mapped_column(ForeignKey('Categories.id'))


async def async_main():
    async with engin.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)