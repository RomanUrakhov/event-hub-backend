from dataclasses import Field, dataclass
from datetime import date
from src.domain.event import Event, EventAdditionalLink
from src.repository.event import IEventRepository, EventNotFound
from src.repository.user_account import IUserAccountRepository
from src.usecases.mappers import event_from_domain_to_usecase


@dataclass
class CreateEventCommand:
    id: str
    name: str
    description: str
    image_id: str | None = Field(default=None)
    owner_account_id: str
    start_date: date
    end_date: date
    additional_links: list[EventAdditionalLink] = Field(default=[])
    participant_ids: list[str] = Field(default=[])


@dataclass
class EventCreatedResult:
    id: str


@dataclass
class EventParticipant:
    id: str
    name: str
    avatar_url: str


@dataclass
class GetEventResult:
    id: str
    name: str
    description: str
    image_id: str | None
    owner_account_id: str
    start_date: date
    end_date: date
    additional_links: list[EventAdditionalLink]
    participants: list[EventParticipant]


def create_event(
    command: CreateEventCommand, event_repo: IEventRepository
) -> EventCreatedResult:
    event = Event.create_new(
        name=command.name,
        image_id=command.image_id,
        owner_account_id=command.owner_account_id,
        start_date=command.start_date,
        end_date=command.end_date,
        additional_links=[
            EventAdditionalLink(name=li.name, link=li.link)
            for li in command.additional_links
        ],
        participant_ids=command.participant_ids,
    )
    try:
        event_repo.create_event(event)
    except Exception:
        pass
    return EventCreatedResult(id_=event.id_)


def get_event(
    event_id: str, event_repo: IEventRepository, user_repo: IUserAccountRepository
) -> GetEventResult:
    event = event_repo.get_by_id(event_id)
    participant_ids = [p.id_ for p in event.participants]
    user_accounts_map = user_repo.get_map_by_participant_ids(
        participant_ids=participant_ids
    )

    event_dto = event_from_domain_to_usecase(event, user_accounts_map)
    return event_dto
