from dataclasses import dataclass, field
from datetime import date

from pydantic import BaseModel, Field, model_validator

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


class CreateEventCommand(BaseModel):
    name: str
    start_date: date
    end_date: date
    image_id: str | None = Field(default=None)
    description: str | None = Field(default=None)
    additional_linls: list[EventAdditionalLink] = Field(default_factory=list)

    @model_validator(mode="after")
    def start_date_before_end_date(self):
        if self.start_date > self.end_date:
            msg = "'start_date' should be before or equal to 'end_date'"
            raise ValueError(msg)
        return self
