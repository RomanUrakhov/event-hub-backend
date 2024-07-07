from domain import Base

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class UserAccount(Base):
    __tablename__ = "user_account"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    twitch_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
