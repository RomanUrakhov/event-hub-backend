from datetime import date
from typing import Optional

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    Field,
    ConfigDict,
    alias_generators,
)


class EventAdditionalLink(BaseModel):
    name: str
    link: AnyHttpUrl


class EventCreateRequest(BaseModel):
    name: str
    description: str
    image_id: str | None = Field(default=None)
    owner_account_id: str
    start_date: date
    end_date: date
    additional_links: list[EventAdditionalLink] = Field(default=[])
    participant_ids: list[str] = Field(default=[])

    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel, populate_by_name=True
    )


class EventCreateResponse(BaseModel):
    id_: str


class Image(BaseModel):
    id_: str
    resource: str


class EventParticipant(BaseModel):
    id_: str
    name: str
    avatar_url: str = Field(default=None)


class GetEventRequest(BaseModel):
    id_: str


class ErrorResponse(BaseModel):
    error_message: str


class BaseEventResponse(BaseModel):
    id_: str
    name: str
    description: str
    image: Optional[Image] = None
    start_date: date
    end_date: date
    additional_links: list[EventAdditionalLink]
    participants: list[EventParticipant]


class GetEventResponse(BaseEventResponse):
    pass


class ListEventsResponse(BaseModel):
    events: list[BaseEventResponse]


class EventNotFoundResponse(BaseModel):
    id_: str
    message: str = Field(default="Can't found Event with such ID")
