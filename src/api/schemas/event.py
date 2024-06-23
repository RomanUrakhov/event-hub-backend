from datetime import date
from typing import Optional
from flask import url_for
from pydantic import BaseModel

from application.interfaces.dao.event import EventDetailsDTO, EventListItemDTO
from domain.models.event import EventAdditionalLink
from domain.models.highlight import Highlight


# TODO: refactor this mess of models (maybe don't give a damn and use domain models as reference)
# TODO: add fields ordering for better client's side expirience


class Image(BaseModel):
    id: str
    url: str

    @classmethod
    def from_image_id(cls, image_id: str | None) -> Optional["Image"]:
        if image_id:
            return cls(
                id=image_id,
                url=url_for("misc.get_image", image_id=image_id, _external=True),
            )
        return None


class GetEventByIdResponse(BaseModel):
    id: str
    name: str
    image: Image | None
    description: str | None
    start_date: date
    end_date: date
    additional_links: list[EventAdditionalLink]
    highligths: list[Highlight]

    @classmethod
    def from_dto(cls, dto: EventDetailsDTO) -> "GetEventByIdResponse":
        return cls(
            id=dto.id,
            name=dto.name,
            image=Image.from_image_id(dto.image_id),
            description=dto.description,
            start_date=dto.start_date,
            end_date=dto.end_date,
            additional_links=dto.additional_links,
            highligths=dto.highlights,
        )


class EventListItem(BaseModel):
    id: str
    name: str
    image: Image | None
    start_date: date
    end_date: date

    @classmethod
    def from_dto(cls, dto: EventListItemDTO) -> "EventListItem":
        return cls(
            id=dto.id,
            name=dto.name,
            image=Image.from_image_id(dto.image_id),
            start_date=dto.start_date,
            end_date=dto.end_date,
        )


class ListAllEventsResponse(BaseModel):
    page_size: int
    total: int
    events: list[EventListItem]

    @classmethod
    def from_dto(cls, dto: list[EventListItemDTO]) -> "ListAllEventsResponse":
        event_items = [EventListItem.from_dto(li) for li in dto]
        items_len = len(event_items)
        return cls(page_size=items_len, total=items_len, events=event_items)
