from apiflask import Schema
from apiflask.fields import String, List, Nested, AbsoluteURLFor, Hyperlinks

from api.schemas.common import EventListItemSchema
from application.interfaces.dao.streamer import StreamerDetailsDTO


class CreateStreamerRequest(Schema):
    twitch_id = String(required=True)
    name = String(required=True)


class CreateStreamerResponse(Schema):
    id = String(required=True)

    url = Hyperlinks(
        {
            "self": AbsoluteURLFor(
                "streamer.get_streamer", values={"streamer_id": "<id>"}, external=True
            )
        }
    )

    @classmethod
    def from_dto(cls, streamer_id: str) -> dict:
        return {"id": streamer_id}


class GetStreamerDetailsResponse(Schema):
    id = String()
    twitch_id = String()
    name = String()

    events = List(Nested(EventListItemSchema))

    @classmethod
    def from_dto(cls, dto: StreamerDetailsDTO) -> dict:
        events = [EventListItemSchema.from_dto(e) for e in dto.events]
        return dict(
            id=dto.id, twitch_id=dto.twitch_id, name=dto.twitch_id, events=events
        )
