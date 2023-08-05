import os

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from sqlalchemy.orm import sessionmaker

from src.bot.FSMmodels import FSMMain
from src.bot.keyboards.user_keyboards import user_kb
from src.bot.lexicon.lexicon_ru import CALLBACK_DATA_LEXICON
from src.bot.parser_logic.parse_wb.parse_wb import ParseWB

router = Router()


@router.message(F.text == 'Отменить')
async def cancel_kb(message: Message, state: FSMContext):
    await state.set_state(FSMMain.start)
    await message.answer('меню', reply_markup=user_kb.create_start_kb())


@router.callback_query(lambda c: c.data == 'cancel')
async def cancel_kb(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.set_state(FSMMain.start)
    await call.message.answer('Меню', reply_markup=user_kb.create_start_kb())


@router.message(F.text == 'настроить парсер')
async def settings_kb(message: Message, session_maker: sessionmaker, state: FSMContext):
    await state.set_state(FSMMain.settings)
    await message.answer('Выбери сайт для парсера\n👇',
                         reply_markup=await user_kb.create_website_list(session_maker=session_maker))


@router.callback_query(FSMMain.settings, lambda c: c.data == F.call_text)
async def choice_website(call: CallbackQuery, session_maker: sessionmaker, state: FSMContext):
    await state.update_data(website=call.data[14:])
    await state.set_state(FSMMain.mode)
    await call.message.edit_text(
        'Выбери способ парсера\n👇',
        reply_markup=await user_kb.create_mode_list(session_maker=session_maker, callback=call.data[14:])
    )


@router.callback_query(FSMMain.mode, lambda c: c.data == F.call_text)
async def choice_mode(call: CallbackQuery, state: FSMContext, bot: Bot):
    bot.parse_mode = None
    await call.message.delete()
    await state.update_data(mode=call.data[14:])
    await state.set_state(FSMMain.url)
    await call.message.answer(
        CALLBACK_DATA_LEXICON[f'{call.data}'],
        reply_markup=user_kb.create_cancel_kb(),
    )
    bot.parse_mode = 'HTML'


@router.message(FSMMain.url)
async def get_url(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    data = await state.get_data()
    await state.set_state(FSMMain.parse)
    await message.answer(
        text=f'<b>Ваши настройки:</b>\n'
             f' <b>сайт</b> - {data["website"]}\n'
             f' <b>способ</b> - {data["mode"]}\n'
             f' <b>полная ссылка</b> - {data["link"]}',
        reply_markup=user_kb.create_parse_kb(),
    )


@router.message(FSMMain.parse, F.text == 'Запустить парсер')
async def start_parse(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.set_state(FSMMain.get_doc)
    await ParseWB(data['link'], message).parse()
    await message.answer('Парсер завершил сбор данных', reply_markup=user_kb.get_document())


@router.message(FSMMain.get_doc, F.text == 'Получить данные в csv')
async def get_document_parse(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(FSMMain.start)
    path = os.path.abspath('wb_data.csv')
    await message.answer('Спасибо, что пользовались мной\n'
                         'Вот данные в csv👇')
    await message.answer_document(FSInputFile(path), reply_markup=user_kb.create_start_kb())
    os.remove(path)
