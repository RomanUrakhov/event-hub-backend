from domain import db

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.models.event import Event
from domain.models.streamer import Streamer


# TODO: add possibility of tracking who won the event (if it's related)
class Participation(db.Model):
    __tablename__ = "participation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[str] = mapped_column(ForeignKey("event.id"), nullable=False)
    streamer_id: Mapped[str] = mapped_column(ForeignKey("streamer.id"), nullable=False)

    streamer: Mapped[Streamer] = relationship("Streamer")
    event: Mapped[Event] = relationship("Event")
