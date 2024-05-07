from src.api.schemas.event import (
    EventCreateRequest,
    EventCreateResponse,
    EventUpdateRequest
)
from src.domain.event import Event
from src.repository.event import IEventRepository


def create_event(event_data: EventCreateRequest, event_repo: IEventRepository) -> EventCreateResponse:
    event = Event.create_new(**event_data.model_dump())
    event_repo.create_event(event)
    return EventCreateResponse(
        id_=event.id_
    )


def update_event(event_data: EventUpdateRequest, event_repo: IEventRepository) -> None:
    current_event = event_repo.get_by_id(event_data.id_)
    current_event.update(**event_data.model_dump(exclude={'id_'}))
    event_repo.update_event(current_event)
