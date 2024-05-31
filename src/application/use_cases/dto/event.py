from dataclasses import dataclass, field
from datetime import date

from src.domain.models.event import EventAdditionalLink


@dataclass
class EventDTO:
    id: str
    name: str
    image_id: str | None
    description: str | None
    start_date: date
    end_date: date
    additional_links: list[EventAdditionalLink] = field(default_factory=list)
