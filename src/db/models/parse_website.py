from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models import Base


class ParseWebsite(Base):
    __tablename__ = 'parse_website_url'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    url: Mapped[str] = mapped_column(Text, unique=True)
    text_callback: Mapped[str] = mapped_column(Text, unique=True)