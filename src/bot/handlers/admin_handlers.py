from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.bot.FSMmodels import FSMMain, FSMAdmin
from src.bot.keyboards.admin_keyboards import admin_kb
from src.bot.keyboards.user_keyboards import user_kb
from src.bot.lexicon.lexicon_ru import ADMIN_PANEL
from src.bot.middlewares.is_admin_middleware import IsAdmin
from src.bot.stuctures.role import Role

router = Router()

router.message.middleware(IsAdmin())


@router.message(F.text == '/admin')
async def start_role_admin(message: Message, state: FSMContext, role: Role):
    await state.set_state(FSMAdmin.admin)
    await message.answer(ADMIN_PANEL['start_admin_panel'],
                         reply_markup=await admin_kb.kb.create_admin_panel(role))


@router.message(F.text == 'Режим админа')
async def start_role_admin(message: Message, state: FSMContext, role: Role):
    await state.set_state(FSMAdmin.admin)
    await message.answer(ADMIN_PANEL['start_admin_panel'],
                         reply_markup=await admin_kb.kb.create_admin_panel(role))


@router.message(FSMAdmin.admin, F.text == 'Админ-панель')
async def start_role_admin(message: Message, state: FSMContext):
    await state.set_state(FSMAdmin.admin_panel)
    await message.answer('Список доступных функций👇',
                         reply_markup=admin_kb.ikb.create_list_functions_admin())


@router.message(FSMAdmin.admin_panel, F.text == 'Отменить')
async def cancel_create_link(message: Message, state: FSMContext, role: Role):
    await state.set_state(FSMAdmin.admin)
    await message.answer(ADMIN_PANEL['start_admin_panel'],
                         reply_markup=await admin_kb.kb.create_admin_panel(role))


@router.callback_query(FSMAdmin.admin_panel, lambda c: c.data == 'set_website')
async def set_website_for_parse(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(FSMAdmin.set_website)
    await call.message.answer('Введите ссылку на сайт',
                              reply_markup=admin_kb.kb.cancel_set_link())


@router.message(FSMAdmin.set_website, F.text == 'Отменить')
async def cancel_create_link(message: Message, state: FSMContext):
    await state.set_state(FSMAdmin.admin_panel)
    await message.answer('Список доступных функций👇',
                         reply_markup=admin_kb.ikb.create_list_functions_admin())


@router.message(FSMAdmin.set_website)
async def cancel_create_link(message: Message, state: FSMContext):
    await state.set_state(FSMAdmin.set_mode)
    await message.answer('Список доступных модов, выберите нужные👇',
                         reply_markup=admin_kb.ikb.create_list_functions_admin())


@router.message(F.text == '/user')
async def start_command_for_role_user(message: Message, state: FSMContext):
    await state.set_state(FSMMain.start)
    await message.answer('Меню\nЧтобы войти в режим админа введите команду /admin',
                         reply_markup=user_kb.create_start_kb())


@router.message(F.text == 'Режим пользователя')
async def start_command_for_role_user(message: Message, state: FSMContext):
    await state.set_state(FSMMain.start)
    await message.answer('Меню\nЧтобы войти в режим админа введите команду /admin',
                         reply_markup=user_kb.create_start_kb())
