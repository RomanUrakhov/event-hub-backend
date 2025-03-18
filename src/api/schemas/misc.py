from apiflask import Schema
from apiflask.fields import File, String, URLFor


class UploadImageSchema(Schema):
    file = File(required=True, description="Image file to upload")


class UploadImageResponseSchema(Schema):
    id = String(required=True, description="Unique identifier of the uploaded image")
    url = URLFor(
        "misc.get_image",
        values={"image_id": "<id>"},
        description="URL to access the uploaded image",
    )
