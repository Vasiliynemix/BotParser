from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.orm import sessionmaker

from src.bot.FSMmodels import FSMMain
from src.bot.keyboards.admin_keyboards import admin_kb
from src.bot.keyboards.user_keyboards import user_kb
from src.bot.stuctures.role import Role
from src.db.queries.queries_admin import get_user_role
from src.db.queries.queries_user import get_user, set_user

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, session_maker: sessionmaker, state: FSMContext):
    if await get_user(message, session_maker) is None:
        await set_user(message, session_maker)
    user_role = await get_user_role(message, session_maker)
    if user_role[0].value == Role.USER.value:
        await state.set_state(FSMMain.start)
        await message.answer('Меню', reply_markup=user_kb.create_start_kb())
    else:
        await message.answer('Меню', reply_markup=admin_kb.kb.create_start_admin_kb())
