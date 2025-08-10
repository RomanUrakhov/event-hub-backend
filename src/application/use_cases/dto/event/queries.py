from datetime import date, datetime
from pydantic import AnyUrl, BaseModel, Field


class EventDetailsAdditionalLink(BaseModel):
    name: str
    url: AnyUrl


class EventDetailsHighlight(BaseModel):
    author_id: str
    url: AnyUrl
    attached_datetime: datetime


class EventDetailsParticipant(BaseModel):
    id: str
    twitch_id: str
    name: str
    avatar_url: str


class EventDetails(BaseModel):
    id: str
    name: str
    image_id: str | None
    description: str | None
    start_date: date
    end_date: date
    additional_links: list[EventDetailsAdditionalLink] = Field(default_factory=list)
    highlights: list[EventDetailsHighlight] = Field(default_factory=list)
    participants: list[EventDetailsParticipant] = Field(default_factory=list)
