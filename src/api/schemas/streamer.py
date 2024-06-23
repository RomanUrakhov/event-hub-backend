from flask import url_for
from pydantic import AnyUrl, BaseModel, PrivateAttr, computed_field


class CreateStreamerResponse(BaseModel):
    id: str
    _url: AnyUrl = PrivateAttr(default=None)

    @computed_field
    @property
    def url(self) -> AnyUrl:
        return url_for("streamer.get_streamer", streamer_id=self.id, _external=True)
