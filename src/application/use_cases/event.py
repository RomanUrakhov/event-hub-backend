from src.application.interfaces.repositories.event import IEventRepository
from src.application.use_cases.dto.event import CreateEventCommand, EventDTO
from src.domain.models.event import Event
from src.application.use_cases.exceptions.event import (
    EventAlreadyExistsException,
    EventNotFoundException,
)


class GetEventById:
    def __init__(self, event_repo: IEventRepository):
        self._event_repo = event_repo

    @staticmethod
    def _map_domain_to_dto(event: Event) -> EventDTO:
        return EventDTO(
            id=event.id,
            name=event.name,
            image_id=event.image_id,
            description=event.description,
            start_date=event.start_date,
            end_date=event.end_date,
            additional_links=event.additional_links,
        )

    def __call__(self, id: str) -> EventDTO:
        event = self._event_repo.get_by_id(id)
        if not event:
            raise EventNotFoundException(event_id=id)
        return self._map_domain_to_dto(event)


EventId = str


class CreateEvent:
    def __init__(self, event_repo: IEventRepository):
        self._event_repo = event_repo

    def __call__(self, data: CreateEventCommand) -> EventId:
        event = data.to_domain()

        existing_event = self._event_repo.get_by_slug(event.slug)
        if existing_event:
            raise EventAlreadyExistsException(event_name=event.name)

        self._event_repo.create(event)
        return event.id
