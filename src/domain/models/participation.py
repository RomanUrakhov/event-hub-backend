from domain import Base

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column


# TODO: add possibility of tracking who won the event (if it's related)
class Participation(Base):
    __tablename__ = "participation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[str] = mapped_column(ForeignKey("event.id"), nullable=False)
    streamer_id: Mapped[str] = mapped_column(ForeignKey("streamer.id"), nullable=False)
