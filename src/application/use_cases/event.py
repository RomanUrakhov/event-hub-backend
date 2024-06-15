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
    EventDTO,
)
from src.domain.models.event import Event


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
