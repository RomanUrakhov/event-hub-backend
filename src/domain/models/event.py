from datetime import date
import re

from domain import Base
from domain.exceptions.event import DuplicatedHightlightException
from domain.models.highlight import Highlight

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property


# I merged domain models with ORM models in purpose to simplify
# development. I know it's not DDD'ish, but my logic is not that complex and
# at this time this implementation seems much more quickier and simplier (maybe)
# TODO: Refactor this part if there's a better solution


class EventAdditionalLink(Base):
    __tablename__ = "additional_link"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[str] = mapped_column(ForeignKey("event.id"), nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=True)


class Event(Base):
    __tablename__ = "event"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    author_id: Mapped[str] = mapped_column(String, nullable=False)
    image_id: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

    additional_links: Mapped[list[EventAdditionalLink]] = relationship(
        "EventAdditionalLink", cascade="all, delete-orphan"
    )
    highlights: Mapped[list[Highlight]] = relationship(
        "Highlight", cascade="all, delete-orphan"
    )

    # TODO: Figure out is 'slug' should be described like this
    # this required me to remove 'slug' column from db but still we can use it...
    @hybrid_property
    def slug(self):
        return re.sub(r"\W+", "-", str(self.name).lower()).strip("-")

    def attach_highlight(self, h: Highlight):
        if h in self.highlights:
            raise DuplicatedHightlightException
        self.highlights.append(h)

    def detach_highlight(self, h: Highlight):
        try:
            self.highlights.remove(h)
        except ValueError:
            pass
