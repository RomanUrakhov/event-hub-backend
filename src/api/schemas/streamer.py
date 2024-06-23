from dataclasses import field
from datetime import date
from flask import url_for
from pydantic import BaseModel, PrivateAttr, computed_field

from application.interfaces.dao.streamer import StreamerDetailsDTO, StreamerEventItem


# TODO: refactor this mess of models (maybe don't give a damn and use domain models as reference)


class CreateStreamerResponse(BaseModel):
    id: str
    _url: str = PrivateAttr(default=None)

    @computed_field
    @property
    def url(self) -> str:
        return url_for("streamer.get_streamer", streamer_id=self.id, _external=True)


class Image(BaseModel):
    id: str
    url: str

    @classmethod
    def from_image_id(cls, image_id: str) -> "Image":
        return cls(
            id=image_id,
            url=url_for("misc.get_image", image_id=image_id, _external=True),
        )


class EventListItem(BaseModel):
    id: str
    name: str
    image: Image | None
    start_date: date  # TODO: change date formatting (i.e. return in ISO format)
    end_date: date

    @classmethod
    def from_dto(cls, event: StreamerEventItem) -> "EventListItem":
        return cls(
            id=event.id,
            name=event.name,
            image=Image.from_image_id(event.image_id),
            start_date=event.start_date,
            end_date=event.end_date,
        )


class GetStreamerDetailsResponse(BaseModel):
    id: str
    twitch_id: str
    name: str

    events: list[EventListItem] = field(default_factory=list)

    @classmethod
    def from_dto(cls, dto: StreamerDetailsDTO) -> "GetStreamerDetailsResponse":
        events = [EventListItem.from_dto(e) for e in dto.events]
        return cls(
            id=dto.id, twitch_id=dto.twitch_id, name=dto.twitch_id, events=events
        )
