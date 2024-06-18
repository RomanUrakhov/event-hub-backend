from application.interfaces.dao.event import (
    EventDetailsDTO,
    EventListItemDTO,
    IEventDAO,
)
from application.interfaces.repositories.participation import IParticipationRepository
from application.interfaces.repositories.streamer import IStreamerRepository
from common.helpers import ulid_from_datetime_utc
from domain.exceptions.event import (
    DuplicatedHightlightException,
    EventAlreadyExistsException,
    EventNotFoundException,
)
from domain.models.highlight import Highlight
from domain.models.participation import Participation
from src.application.interfaces.repositories.event import IEventRepository
from src.application.use_cases.dto.event import (
    AttachHighlightsCommand,
    CreateEventCommand,
    EntrollStreamerOnEventCommand,
)


class GetEventById:
    def __init__(self, event_dao: IEventDAO):
        self._event_dao = event_dao

    def __call__(self, event_id: str) -> EventDetailsDTO:
        event_dto = self._event_dao.get_event(event_id)
        if not event_dto:
            raise EventNotFoundException(event_id=event_id)
        return event_dto


class ListAllEvents:
    def __init__(self, event_dao: IEventDAO):
        self._event_dao = event_dao

    def __call__(self) -> list[EventListItemDTO]:
        event_dtos = self._event_dao.list_events()
        return event_dtos


EventId = str


class CreateEvent:
    def __init__(
        self,
        event_repo: IEventRepository,
        streamer_repository: IStreamerRepository,
        participation_repository: IParticipationRepository,
    ):
        self._event_repo = event_repo
        self._streamer_repo = streamer_repository
        self._participation_repo = participation_repository

    def __call__(self, data: CreateEventCommand) -> EventId:
        event = data.to_domain()

        existing_event = self._event_repo.get_by_slug(event.slug)
        if existing_event:
            raise EventAlreadyExistsException(event_name=event.name)

        self._event_repo.create(event)

        if data.streamers_ids:
            streamers = self._streamer_repo.list_by_ids(data.streamers_ids)
            participations = [
                Participation(ulid_from_datetime_utc(), event.id, s.id)
                for s in streamers
            ]
            if participations:
                self._participation_repo.save_batch(participations)

        return event.id


class EntrollStreamersOnEvent:
    def __init__(
        self,
        event_repo: IEventRepository,
        streamer_repository: IStreamerRepository,
        participation_repository: IParticipationRepository,
    ):
        self._event_repo = event_repo
        self._streamer_repo = streamer_repository
        self._participation_repo = participation_repository

    def __call__(self, data: EntrollStreamerOnEventCommand):
        event = self._event_repo.get_by_id(data.event_id)
        if not event:
            raise EventNotFoundException

        streamers = self._streamer_repo.list_by_ids(data.streamers_ids)

        participations = [
            Participation(ulid_from_datetime_utc(), event_id=event.id, streamer_id=s.id)
            for s in streamers
        ]

        if participations:
            self._participation_repo.save_batch(participations)


class AttachHightlihtsToEvent:
    def __init__(self, event_repository: IEventRepository):
        self._event_repo = event_repository

    def __call__(self, data: AttachHighlightsCommand):
        event = self._event_repo.get_by_id(data.event_id)

        if not event:
            raise EventNotFoundException

        for highlight in data.highlights:
            try:
                event.attach_highlight(
                    Highlight(url=highlight.url, author_id=highlight.author_id)
                )
            except DuplicatedHightlightException:
                pass

        self._event_repo.update(event)
