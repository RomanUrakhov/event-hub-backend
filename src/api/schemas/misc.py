from apiflask import Schema
from apiflask.fields import File

from api.schemas.common import ImageSchema


class UploadImageSchema(Schema):
    file = File(required=True, description="Image file to upload")


class UploadImageResponseSchema(ImageSchema):
    pass
