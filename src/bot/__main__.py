import asyncio
import logging

from aiogram import Bot, Dispatcher

from src.bot.handlers import start_handler, settings_parse_handlers, admin_handlers
from src.configuration import conf
from src.db.database import create_session_maker, async_engine


async def run_bot():
    bot: Bot = Bot(token=conf.bot.token, parse_mode='HTML')

    dp: Dispatcher = Dispatcher()

    dp.include_router(admin_handlers.router)
    dp.include_router(start_handler.router)
    dp.include_router(settings_parse_handlers.router)

    engine = async_engine(url=conf.db.build_url_for_db())
    session_maker = create_session_maker(engine=engine)

    await dp.start_polling(bot, session_maker=session_maker)


if __name__ == '__main__':
    logging.basicConfig(level=conf.logging_level)
    asyncio.run(run_bot())
