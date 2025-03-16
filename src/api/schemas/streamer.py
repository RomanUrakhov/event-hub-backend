from flask import url_for
from apiflask import Schema
from apiflask.fields import String, List, Nested, Date
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


class Image(Schema):
    id = String()
    url = String()

    @classmethod
    def from_image_id(cls, image_id: str | None) -> dict | None:
        if not image_id:
            return None
        return dict(
            id=image_id,
            url=url_for("misc.get_image", image_id=image_id, _external=True),
        )


class EventListItem(Schema):
    id = String()
    name = String()
    image = Nested(Image, nullable=True)
    start_date = Date()  # TODO: change date formatting (i.e. return in ISO format)
    end_date = Date()

    @classmethod
    def from_dto(cls, event: StreamerEventItem) -> dict:
        return dict(
            id=event.id,
            name=event.name,
            image=Image.from_image_id(event.image_id),
            start_date=event.start_date,
            end_date=event.end_date,
        )


class GetStreamerDetailsResponse(Schema):
    id = String()
    twitch_id = String()
    name = String()

    events = List(Nested(EventListItem))

    @classmethod
    def from_dto(cls, dto: StreamerDetailsDTO) -> dict:
        events = [EventListItem.from_dto(e) for e in dto.events]
        return dict(
            id=dto.id, twitch_id=dto.twitch_id, name=dto.twitch_id, events=events
        )
