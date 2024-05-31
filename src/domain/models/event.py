from dataclasses import field, dataclass
from datetime import date


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
