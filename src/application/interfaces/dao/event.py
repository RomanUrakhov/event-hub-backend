from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date

from domain.models.event import EventAdditionalLink
from domain.models.highlight import Highlight


@dataclass
class EventDetailsDTO:
    id: str
    name: str
    image_id: str | None
    description: str | None
    start_date: date
    end_date: date
    additional_links: list[EventAdditionalLink] = field(default_factory=list)
    highlights: list[Highlight] = field(default_factory=list)


@dataclass
class EventListItemDTO:
    id: str
    name: str
    image_id: str | None
    start_date: date
    end_date: date


class IEventDAO(ABC):
    @abstractmethod
    def get_event(self, id: str) -> EventDetailsDTO:
        pass

    @abstractmethod
    def list_events(self) -> list[EventListItemDTO]:
        pass
