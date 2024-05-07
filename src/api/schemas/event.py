from datetime import date

from pydantic import BaseModel, Field


class EventAdditionalLink(BaseModel):
    name: str
    link: str


class EventCreateRequest(BaseModel):
    name: str
    description: str
    image_id: str | None = Field(default=None)
    owner_account_id: str = Field(alias='ownerAccountId')
    start_date: date = Field(alias='startDate')
    end_date: date = Field(alias='endDate')
    additional_links: list[EventAdditionalLink] = Field(default=[], alias='additionalLinks')
    participant_ids: list[str] = Field(default=[], alias='participantIds')


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
