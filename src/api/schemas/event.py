from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, alias_generators, field_validator, root_validator, model_validator

from src.domain.event import Event


class EventAdditionalLink(BaseModel):
    name: str
    link: str


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
        alias_generator=alias_generators.to_camel,
        populate_by_name=True
    )


class EventUpdateRequest(BaseModel):
    id_: str
    name: str
    description: str
    image_id: str
    start_date: date
    end_date: date
    additional_links: list[EventAdditionalLink]
    participant_ids: list[str]


class EventCreateResponse(BaseModel):
    id_: str


class EventParticipant(BaseModel):
    id_: str
    name: str
    avatar_url: str


class Image(BaseModel):
    id_: str
    resource: str


class GetEventRequest(BaseModel):
    id_: str


class ErrorResponse(BaseModel):
    error_message: str


class EventResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id_: str
    name: str
    description: str
    image: Optional[Image] = None
    start_date: date
    end_date: date
    additional_links: list[EventAdditionalLink]
    participants: list[EventParticipant]


class EventNotFoundResponse(BaseModel):
    id_: str
    message: str = Field(default="Can't found Event with such ID")


class ListEventsResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    events: list[EventResponse]
