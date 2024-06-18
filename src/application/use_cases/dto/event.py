from datetime import date

from pydantic import AnyUrl, BaseModel, Field, model_validator

from domain.models.highlight import Highlight
from src.common.helpers import ulid_from_datetime_utc
from src.domain.models.event import Event, EventAdditionalLink


class EventAdditionalLinkModel(BaseModel):
    name: str
    link: AnyUrl


# TODO: perhaps it's better to define such models in api/schemas
class CreateEventCommand(BaseModel):
    name: str
    start_date: date
    end_date: date
    image_id: str | None = Field(default=None)
    description: str | None = Field(default=None)
    additional_links: list[EventAdditionalLinkModel] = Field(default_factory=list)
    streamers_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def start_date_before_end_date(self):
        if self.start_date > self.end_date:
            msg = "'start_date' should be before or equal to 'end_date'"
            raise ValueError(msg)
        return self

    def to_domain(self) -> Event:
        return Event(
            id=ulid_from_datetime_utc(),
            name=self.name,
            start_date=self.start_date,
            end_date=self.end_date,
            image_id=self.image_id,
            description=self.description,
            additional_links=[
                EventAdditionalLink(url=li.url, name=li.name)
                for li in self.additional_links
            ],
        )


class EntrollStreamerOnEventCommand(BaseModel):
    event_id: str
    streamers_ids: list[str]


class HightlightModel(BaseModel):
    url: AnyUrl


class AttachHighlightsCommand(BaseModel):
    event_id: str
    highlights: list[Highlight]
