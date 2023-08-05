from dataclasses import dataclass

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.orm import sessionmaker

from src.bot.filters.callback_website_filter import CallbackWebsiteFilter
from src.db.queries.queries_website import get_website_list, get_mods_list


class Keyboard:
    @staticmethod
    def create_start_kb():
        start_kb = [
            [KeyboardButton(text='настроить парсер')],
            [KeyboardButton(text='Текст')]
        ]
        return ReplyKeyboardMarkup(keyboard=start_kb,
                                   resize_keyboard=True,
                                   input_field_placeholder='Выберите один из вариантов👇',
                                   one_time_keyboard=True)

    @staticmethod
    def create_cancel_kb():
        cancel_kb = [
            [KeyboardButton(text='Отменить')],
        ]
        return ReplyKeyboardMarkup(keyboard=cancel_kb,
                                   resize_keyboard=True,
                                   input_field_placeholder='Если хотите отменить настройки нажмите Отменить👇',
                                   one_time_keyboard=True)

    @staticmethod
    def create_parse_kb():
        parse_kb = [
            [KeyboardButton(text='Запустить парсер')],
            [KeyboardButton(text='Отменить')]
        ]
        return ReplyKeyboardMarkup(keyboard=parse_kb,
                                   resize_keyboard=True,
                                   input_field_placeholder='Если хотите отменить настройки нажмите Отменить👇',
                                   one_time_keyboard=True)

    @staticmethod
    def get_document():
        get_result_kb = [
            [KeyboardButton(text='Получить данные в csv')]
        ]
        return ReplyKeyboardMarkup(keyboard=get_result_kb,
                                   resize_keyboard=True,
                                   input_field_placeholder='Чтобы получить данные нажмите на кнопку👇',
                                   one_time_keyboard=True)

    @staticmethod
    async def create_website_list(session_maker: sessionmaker):
        kb_get_all_website = InlineKeyboardBuilder()
        website_url_list = await get_website_list(session_maker=session_maker)
        for text_callback in website_url_list:
            kb_get_all_website.button(text=text_callback[0],
                                      callback_data=CallbackWebsiteFilter(call_text=text_callback[0]))
        kb_get_all_website.button(text='Отменить', callback_data='cancel')
        kb_get_all_website.adjust(2)
        return kb_get_all_website.as_markup(resize_keyboard=True,
                                            one_time_keyboard=True)

    @staticmethod
    async def create_mode_list(session_maker: sessionmaker, callback):
        kb_mode = InlineKeyboardBuilder()
        mods_list = await get_mods_list(session_maker=session_maker, callback=callback)
        for text_callback in mods_list:
            kb_mode.button(text=text_callback[0],
                           callback_data=CallbackWebsiteFilter(call_text=text_callback[0]))
        kb_mode.button(text='Отменить', callback_data='cancel')
        kb_mode.adjust(1)
        return kb_mode.as_markup(resize_keyboard=True,
                                 one_time_keyboard=True)


user_kb = Keyboard()
