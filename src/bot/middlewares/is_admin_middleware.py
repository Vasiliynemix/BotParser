from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from src.bot.stuctures.role import Role
from src.db.queries.queries_admin import get_user_role


class IsAdmin(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        session_maker = data['session_maker']
        user_role = await get_user_role(message=event, session_maker=session_maker)
        data['role'] = user_role[0].value
        if user_role[0].value == Role.USER.value:
            await event.answer('У вас нет прав пользоваться данной функцией, извините')
            return False

        return await handler(event, data)
