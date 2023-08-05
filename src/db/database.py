from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.configuration import conf


def async_engine(url: URL | str) -> AsyncEngine:
    return create_async_engine(url=url, echo=conf.debug, pool_pre_ping=True)


def create_session_maker(engine: AsyncEngine | None) -> sessionmaker:
    return sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession
    )