from domain import Base

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class Participation(Base):
    __tablename__ = "participation"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    event_id: Mapped[str] = mapped_column(ForeignKey("events.id"), nullable=False)
    streamer_id: Mapped[str] = mapped_column(ForeignKey("streamers.id"), nullable=False)
    is_winner: Mapped[bool] = mapped_column(Boolean, default=False)

    # TODO: Where to put logic of checking that event can have only one winner?
