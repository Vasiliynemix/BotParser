from dataclasses import dataclass

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.stuctures.role import Role


class ReplyKeyboardAdmin:
    @staticmethod
    def create_start_admin_kb():
        start_kb = [
            [KeyboardButton(text='Режим админа')],
            [KeyboardButton(text='Режим пользователя')],
        ]
        return ReplyKeyboardMarkup(keyboard=start_kb,
                                   resize_keyboard=True,
                                   input_field_placeholder='Выберите один из вариантов👇',
                                   one_time_keyboard=True)

    @staticmethod
    async def create_admin_panel(role: Role):
        if role == 2:
            admin_panel = [
                [KeyboardButton(text='Админ-панель')],
                [KeyboardButton(text='Добавить админа')],
            ]
        else:
            admin_panel = [
                [KeyboardButton(text='Админ-панель')]
            ]
        return ReplyKeyboardMarkup(keyboard=admin_panel,
                                   resize_keyboard=True,
                                   input_field_placeholder='Выберите один из вариантов👇',
                                   one_time_keyboard=True)

    @staticmethod
    def cancel_set_link():
        cancel_kb = [
            [KeyboardButton(text='Отменить')]
        ]
        return ReplyKeyboardMarkup(keyboard=cancel_kb,
                                   resize_keyboard=True,
                                   input_field_placeholder='Если хотите отменить создание ссылки нажмите Отменить👇',
                                   one_time_keyboard=True)


class InlineKeyboardAdmin:
    @staticmethod
    def create_list_functions_admin():
        functions_admin = InlineKeyboardBuilder()
        functions_admin.button(text='Добавить сайт для парсера', callback_data='set_website')
        functions_admin.button(text='Удалить сайт для парсера', callback_data='delete_website')
        functions_admin.button(text='Список доступных парсеров', callback_data='get_all_website')
        functions_admin.adjust(2)
        return functions_admin.as_markup(resize_keyboard=True,
                                         one_time_keyboard=True)

    @staticmethod
    def set_mode_for_website():
        list_kb = InlineKeyboardBuilder()
        list_kb.button(text='1', callback_data='1')
        return list_kb.as_markup(resize_keyboard=True,
                                 one_time_keyboard=True)


class KeyboardAdmin:
    kb: ReplyKeyboardAdmin = ReplyKeyboardAdmin()
    ikb: InlineKeyboardAdmin = InlineKeyboardAdmin()


admin_kb = KeyboardAdmin()
