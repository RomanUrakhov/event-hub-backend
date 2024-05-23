from src.domain.event import Event
from src.domain.user_account import UserAccount
from src.usecases.event_cases import EventParticipant, GetEventResult


def event_from_domain_to_usecase(
    event: Event, users_map: dict[str, UserAccount]
) -> GetEventResult:
    return GetEventResult(
        id=event.id_,
        name=event.name,
        description=event.description,
        image_id=event.image_id,
        start_date=event.start_date,
        end_date=event.end_date,
        owner_account_id=event.owner_account_id,
        additional_links=event.additional_links,
        participants=[
            EventParticipant(
                id=p.id, name=p.name, avatar_url=users_map.get(p.id).avatar_url
            )
            for p in event.participants
        ],
    )
