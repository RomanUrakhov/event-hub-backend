from apiflask import Schema
from apiflask.fields import String, Nested, Date, AbsoluteURLFor


class ImageSchema(Schema):
    id = String(required=True)
    url = AbsoluteURLFor("misc.get_image", values={"image_id": "<id>"}, required=True)

    @classmethod
    def from_image_id(cls, image_id: str | None):
        if image_id:
            return {"id": image_id}
        return None


class EventListItemSchema(Schema):
    id = String(required=True)
    name = String(required=True)
    image = Nested(ImageSchema, nullable=True)
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
