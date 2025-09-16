from pydantic import AnyUrl, TypeAdapter
from application.interfaces.dao.event import (
    EventListItemDTO,
    IEventDAO,
)
from application.interfaces.repositories.account import (
    IAccountAppAccessRepository,
    IAccountEventAccessRepository,
)
from application.interfaces.repositories.participation import IParticipationRepository
from application.interfaces.repositories.streamer import IStreamerRepository
from application.interfaces.services.twitch_service import ITwitchService
from application.use_cases.dto.event.queries import (
    EventDetailsAdditionalLink,
    EventDetailsHighlight,
    EventDetailsParticipant,
    EventDetails,
)
from common.helpers import ulid_from_datetime_utc
from domain.exceptions.account import (
    AccountDoesNotHaveAccessException,
    AccountDoesNotHaveCreatorAccessException,
)
from domain.exceptions.event import (
    DuplicatedHightlightException,
    EventAlreadyExistsException,
    EventNotFoundException,
)
from domain.models.highlight import Highlight
from domain.models.participation import Participation
from src.application.interfaces.repositories.event import IEventRepository
from application.use_cases.dto.event.commands import (
    AttachHighlightsCommand,
    CreateEventCommand,
    EntrollStreamerOnEventCommand,
)


class GetEventById:
    def __init__(self, event_dao: IEventDAO, twitch_service: ITwitchService):
        self._event_dao = event_dao
        self._twitch_service = twitch_service

    def __call__(self, event_id: str) -> EventDetails:
        event_dao_dto = self._event_dao.get_event(event_id)
        if not event_dao_dto:
            raise EventNotFoundException(event_id=event_id)

        event = EventDetails(
            id=event_dao_dto.id,
            name=event_dao_dto.name,
            start_date=event_dao_dto.start_date,
            end_date=event_dao_dto.end_date,
            image_id=event_dao_dto.image_id,
            description=event_dao_dto.description,
            additional_links=[
                EventDetailsAdditionalLink(
                    name=li.name, url=TypeAdapter(AnyUrl).validate_strings(li.url)
                )
                for li in event_dao_dto.additional_links
            ],
            highlights=[
                EventDetailsHighlight(
                    author_id=h.author_id,
                    url=TypeAdapter(AnyUrl).validate_strings(h.url),
                    attached_datetime=h.attached_datetime,
                )
                for h in event_dao_dto.highlights
            ],
        )

        if event_dao_dto.participants:
            twitch_ids = [
                p.twitch_id for p in event_dao_dto.participants if p.twitch_id
            ]
            twitch_users_map = {
                u.id: u for u in self._twitch_service.list_users_by_ids(twitch_ids)
            }

            event_participants = [
                EventDetailsParticipant(
                    id=participant.streamer_id,
                    twitch_id=participant.twitch_id,
                    name=twitch_users_map[participant.twitch_id].display_name,
                    avatar_url=twitch_users_map[participant.twitch_id].avatar_url,
                )
                for participant in event_dao_dto.participants
            ]

            event.participants = event_participants

        return event


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
        account_app_access_repo: IAccountAppAccessRepository,
    ):
        self._event_repo = event_repo
        self._streamer_repo = streamer_repository
        self._participation_repo = participation_repository
        self._account_app_access_repo = account_app_access_repo

    def __call__(self, data: CreateEventCommand) -> EventId:
        account_app_access = self._account_app_access_repo.account_has_global_access(
            data.author_id
        )
        if not account_app_access:
            raise AccountDoesNotHaveCreatorAccessException(account_id=data.author_id)

        event = data.to_domain()

        existing_event = self._event_repo.get_by_slug(event.slug)
        if existing_event:
            raise EventAlreadyExistsException(event_name=event.name)

        self._event_repo.create(event)

        if data.streamers_ids:
            streamers = self._streamer_repo.list_by_ids(data.streamers_ids)
            participations = [
                Participation(event_id=event.id, streamer_id=s.id) for s in streamers
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
        account_event_access_repository: IAccountEventAccessRepository,
    ):
        self._event_repo = event_repo
        self._streamer_repo = streamer_repository
        self._participation_repo = participation_repository
        self._account_event_access_repo = account_event_access_repository

    def __call__(self, data: EntrollStreamerOnEventCommand):
        event = self._event_repo.get_by_id(data.event_id)
        if not event:
            raise EventNotFoundException(event_id=data.event_id)

        account_access = self._account_event_access_repo.get_account_access(
            account_id=data.author_id, event_id=event.id
        )
        if not account_access:
            raise AccountDoesNotHaveAccessException(
                account_id=data.author_id, event_id=event.id
            )
        if not account_access.can_enroll_streamers_on_event():
            raise AccountDoesNotHaveAccessException(
                account_id=data.author_id, event_id=event.id
            )

        streamers = self._streamer_repo.list_by_ids(data.streamers_ids)

        participations = [
            Participation(ulid_from_datetime_utc(), event_id=event.id, streamer_id=s.id)
            for s in streamers
        ]

        if participations:
            self._participation_repo.save_batch(participations)


class AttachHightlihtsToEvent:
    def __init__(
        self,
        event_repository: IEventRepository,
        account_event_access_repository: IAccountEventAccessRepository,
    ):
        self._event_repo = event_repository
        self._account_event_access_repo = account_event_access_repository

    def __call__(self, data: AttachHighlightsCommand) -> list[str]:
        event = self._event_repo.get_by_id(data.event_id)

        if not event:
            raise EventNotFoundException(event_id=data.event_id)

        account_access = self._account_event_access_repo.get_account_access(
            account_id=data.author_id, event_id=event.id
        )
        if not account_access or not account_access.can_moderate_highlights_on_event():
            raise AccountDoesNotHaveAccessException(
                account_id=data.author_id, event_id=event.id
            )

        highlights = [
            Highlight(
                url=str(h.url),
                author_id=data.author_id,
            )
            for h in data.highlights
        ]

        attached_highlights = []
        for highlight in highlights:
            try:
                event.attach_highlight(
                    Highlight(url=highlight.url, author_id=highlight.author_id)
                )
                attached_highlights.append(highlight.url)
            except DuplicatedHightlightException:
                pass

        self._event_repo.update(event)

        return attached_highlights
