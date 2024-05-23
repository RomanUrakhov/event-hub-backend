from flask import url_for
from src.api.schemas.event import (
    EventAdditionalLink,
    EventParticipant,
    GetEventResponse,
    Image,
)
from src.usecases.event_cases import GetEventResult


def event_from_usecase_to_api_response(event: GetEventResult) -> GetEventResponse:
    return GetEventResponse(
        id_=event.id_,
        name=event.name,
        description=event.description,
        image=Image(
            id_=event.image_id, resource=f"{url_for('get_event')}/{event.image_id}"
        )
        if event.image_id
        else None,
        start_date=event.start_date,
        end_date=event.end_date,
        additional_links=[
            EventAdditionalLink(name=link.name, link=link.link)
            for link in event.additional_links
        ],
        participants=[
            EventParticipant(id_=p.id_, name=p.name, avatar_url=p.avatar_url)
            for p in event.participants
        ],
    )
