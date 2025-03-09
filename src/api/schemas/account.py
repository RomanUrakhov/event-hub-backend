from pydantic import BaseModel
from typing import Dict


class EventAccessSchema(BaseModel):
    can_enroll_streamers: bool
    can_moderate_highlights: bool


class AccountAccessSchema(BaseModel):
    global_access: bool
    events: Dict[str, EventAccessSchema]


class EventSpecificAccessSchema(BaseModel):
    event_id: str
    can_enroll_streamers: bool
    can_moderate_highlights: bool
