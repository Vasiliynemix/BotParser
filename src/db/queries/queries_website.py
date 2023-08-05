import re

from sqlalchemy import select, Result
from sqlalchemy.dialects.postgresql import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.db.models import ParseWebsite, ParseMode


async def get_website_list(session_maker: sessionmaker):
    async with session_maker() as session:
        session: AsyncSession
        query = await session.execute(select(ParseWebsite.text_callback))
        query: Result[Any]
        return query.all()


async def get_mods_list(session_maker: sessionmaker, callback):
    async with session_maker() as session:
        session: AsyncSession
        query = await session.execute(select(ParseMode.mode).
                                      where(ParseMode.callback == callback))
        query: Result[Any]
        return query.all()


# async def create_text_callback(session_maker: sessionmaker):
#     async with session_maker() as session:
#         query = await session.execute(select(ParseWebsite))
#         website = re.findall(r'\w+', ParseWebsite.url)
#         return website[2]