# TODO: refactor this mess of models (maybe don't give a damn and use domain models as reference)
# TODO: add fields ordering for better client's side expirience

from apiflask import Schema
from apiflask.fields import String, List, Date, Nested, URL, Integer, URLFor
from apiflask.validators import Length, OneOf
from apiflask.validators import URL as URLValidator
from marshmallow import ValidationError, validates_schema


class ImageSchema(Schema):
    id = String(required=True)
    url = URLFor("misc.get_image", values={"image_id": "<id>"}, _external=True)

    @classmethod
    def from_image_id(cls, image_id: str | None):
        if image_id:
            return {"id": image_id}
        return None


class GetEventByIdHighlightSchema(Schema):
    author_id = String(required=True)
    url = URL(required=True, validate=URLValidator())
    attached_datetime = Date(required=True)


class GetEventByIdAdditionalLinkSchema(Schema):
    url = URL(required=True, validate=URLValidator())
    name = String(required=True)


class GetEventByIdResponseSchema(Schema):
    id = String(required=True)
    name = String(required=True)
    image = Nested(ImageSchema, allow_none=True)
    description = String(allow_none=True)
    start_date = Date(required=True)
    end_date = Date(required=True)
    additional_links = List(Nested(GetEventByIdAdditionalLinkSchema))
    highlights = List(Nested(GetEventByIdHighlightSchema))

    @classmethod
    def from_dto(cls, dto):
        return {
            "id": dto.id,
            "name": dto.name,
            "image": ImageSchema.from_image_id(dto.image_id),
            "description": dto.description,
            "start_date": dto.start_date,
            "end_date": dto.end_date,
            "additional_links": [
                {"url": li.url, "name": li.name} for li in dto.additional_links
            ],
            "highlights": [
                {
                    "author_id": h.author_id,
                    "url": h.url,
                    "attached_datetime": h.attached_datetime,
                }
                for h in dto.highlights
            ],
        }


class EventListItemSchema(Schema):
    id = String(required=True)
    name = String(required=True)
    image = Nested(ImageSchema, allow_none=True)
    start_date = Date(required=True)
    end_date = Date(required=True)

    @classmethod
    def from_dto(cls, dto):
        return {
            "id": dto.id,
            "name": dto.name,
            "image": ImageSchema.from_image_id(dto.image_id),
            "start_date": dto.start_date,
            "end_date": dto.end_date,
        }


class ListAllEventsResponseSchema(Schema):
    page_size = Integer(required=True)
    total = Integer(required=True)
    events = List(Nested(EventListItemSchema))

    @classmethod
    def from_dto(cls, dto_list):
        event_items = [EventListItemSchema.from_dto(li) for li in dto_list]
        return {
            "page_size": len(event_items),
            "total": len(event_items),
            "events": event_items,
        }


class EventAdditionalLinkSchema(Schema):
    url = URL(required=True, description="Additional link URL")
    name = String(
        required=False, validate=Length(min=3, max=30), description="Name of the link"
    )


class CreateEventRequestSchema(Schema):
    name = String(
        required=True, validate=Length(min=1), description="Name of the event"
    )
    start_date = Date(
        required=True,
        description="Start date (YYYY-MM-DD)<br>`start_date` must be **less than or equal to** `end_date`.",
    )
    end_date = Date(
        required=True,
        description="End date (YYYY-MM-DD)<br>`end_date` must be **greater than or equal to** `start_date`.",
    )
    image_id = String(required=False, allow_none=True, description="Optional image ID")
    description = String(
        required=False, allow_none=True, description="Optional event description"
    )
    additional_links = List(
        Nested(EventAdditionalLinkSchema),
        required=False,
        description="List of additional links",
    )
    streamers_ids = List(
        String,
        required=False,
        description="List of streamer IDs to enroll initially at event creation",
    )

    @validates_schema
    def validate_dates(self, data, **kwargs):
        """Ensure that start_date is before or equal to end_date."""
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date and end_date and start_date > end_date:
            raise ValidationError(
                "'start_date' should be before or equal to 'end_date'",
                field_name="start_date",
            )


class CreateEventResponseSchema(Schema):
    id = String(required=True)
    url = URL(required=True)


class EnrollStreamerRequestSchema(Schema):
    streamer_id = String(required=True, description="Streamer ID to enroll")


class AttachHighlightsRequestSchema(Schema):
    highlight_urls = List(URL, required=True, description="List of highlight URLs")


class AttachHighlightsResponseSchema(Schema):
    event_id = String(required=True)
    highlights = List(URL, required=True)
