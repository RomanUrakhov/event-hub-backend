from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class EventDetailsAdditionalLinkDTO:
    url: str
    name: str


@dataclass
class EventDetailsHighlightDTO:
    author_id: str
    url: str
    attached_datetime: datetime


@dataclass
class EventDetailsDTO:
    id: str
    name: str
    image_id: str | None
    description: str | None
    start_date: date
    end_date: date
    additional_links: list[EventDetailsAdditionalLinkDTO] = field(default_factory=list)
    highlights: list[EventDetailsHighlightDTO] = field(default_factory=list)


@dataclass
class EventListItemDTO:
    id: str
    name: str
    image_id: str | None
    start_date: date
    end_date: date


class IEventDAO(ABC):
    @abstractmethod
    def get_event(self, id: str) -> EventDetailsDTO | None:
        pass

    @abstractmethod
    def list_events(self) -> list[EventListItemDTO]:
        pass
