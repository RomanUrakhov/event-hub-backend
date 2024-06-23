from pydantic import BaseModel


class CreateStreamerCommand(BaseModel):
    twitch_id: str
    name: str
