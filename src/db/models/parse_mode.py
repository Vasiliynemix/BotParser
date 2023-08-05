from sqlalchemy import Integer, BigInteger, ForeignKey, Text, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models import Base


class ParseMode(Base):
    __tablename__ = 'mods'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id'))
    mode: Mapped[str] = mapped_column(String(30))
    callback: Mapped[str] = mapped_column(Text, ForeignKey('parse_website_url.text_callback'))
