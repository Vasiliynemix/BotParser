from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from src.db.models import User


async def get_user_role(message: Message, session_maker: sessionmaker):
    async with session_maker() as session:
        query = await session.execute(select(User.role).where(User.user_id == message.from_user.id))
        return query.one_or_none()