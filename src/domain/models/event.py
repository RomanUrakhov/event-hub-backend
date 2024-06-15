from dataclasses import field, dataclass
from datetime import date
import re

from domain.exceptions.event import DuplicatedHightlightException
from domain.models.highlight import Highlight


@dataclass(frozen=True)
class EventAdditionalLink:
    url: str
    name: str


@dataclass
class Event:
    id: str
    name: str
    start_date: date
    end_date: date
    image_id: str | None = field(default=None)
    description: str | None = field(default=None)
    additional_links: list[EventAdditionalLink] = field(default_factory=list)

    highlights: list[Highlight] = field(default_factory=list)

    @property
    def slug(self) -> str:
        slug_ = self.name.lower()
        slug_ = re.sub(r"\W+", "-", slug_)
        slug_ = slug_.strip("-")
        return slug_

    def attach_highlight(self, h: Highlight):
        if h in self.highlights:
            raise DuplicatedHightlightException
        self.highlights.append(h)

    def detach_highlight(self, h: Highlight):
        try:
            self.highlights.remove(h)
        except ValueError:
            pass
