import os

from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from src.bot.stuctures.role import Role
from src.db.models import User


async def get_user(message: Message, session_maker: sessionmaker):
    async with session_maker() as session:
        query = await session.execute(select(User).where(User.user_id == message.from_user.id))
        return query.one_or_none()


async def set_user(message: Message, session_maker: sessionmaker):
    async with session_maker() as session:
        await session.execute(select(User))
        if message.from_user.id == int(os.getenv('SUPER_ADMIN')):
            user = User(
                user_id=message.from_user.id,
                username=message.from_user.username,
                role=Role.SUPER_ADMIN,
            )
        else:
            user = User(
                user_id=message.from_user.id,
                username=message.from_user.username,
            )

        await session.merge(user)
        await session.commit()
        return True