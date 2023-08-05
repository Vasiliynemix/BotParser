from aiogram.fsm.state import StatesGroup, State


class FSMMain(StatesGroup):
    start = State()
    settings = State()
    mode = State()
    url = State()
    parse = State()
    get_doc = State()


class FSMAdmin(StatesGroup):
    admin = State()
    admin_panel = State()
    set_website = State()
    set_mode = State()
