from datetime import date
from flask import url_for
from pydantic import BaseModel, AnyUrl

from src.application.use_cases.dto.event import EventDTO


class Image(BaseModel):
    id: str
    url: str


class EventAdditionalLink(BaseModel):
    name: str
    url: AnyUrl


class GetEventByIdResponse(BaseModel):
    id: str
    name: str
    image: Image | None
    description: str | None
    start_date: date
    end_date: date
    additional_links: list[EventAdditionalLink]

    @classmethod
    def from_dto(cls, dto: EventDTO) -> "GetEventByIdResponse":
        return cls(
            id=dto.id,
            name=dto.name,
            image=(
                Image(id=dto.image_id, url=url_for("misc.get_image"))
                if dto.image_id
                else None
            ),
            description=dto.description,
            start_date=dto.start_date,
            end_date=dto.end_date,
            additional_links=[
                EventAdditionalLink(name=li.name, url=li.url)
                for li in dto.additional_links
            ],
        )
