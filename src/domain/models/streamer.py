from domain import db

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Streamer(db.Model):
    __tablename__ = "streamer"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    twitch_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
