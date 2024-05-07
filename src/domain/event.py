import dataclasses
from datetime import date
from uuid import uuid4


class EventAdditionalLink:
    def __init__(self, name: str, link: str):
        self.name = name
        self.link = link


@dataclasses.dataclass
class EventParticipant:
    id_: str
    name: str
    avatar_url: str


class EventIcon:
    def __init__(self, file_id: str):
        self.file_id = file_id


class Event:
    def __init__(
        self,
        id_: str,
        name: str,
        image_id: str,
        description: str,
        owner_account_id: str,
        start_date: date,
        end_date: date,
        additional_links: list[EventAdditionalLink],
        participants: list[EventParticipant]
    ):
        self.id_ = id_
        self.name = name
        self.description = description
        self.image_id = image_id
        self.owner_account_id = owner_account_id
        self.start_date = start_date
        self.end_date = end_date
        self.additional_links = additional_links
        self.participants = participants

    @staticmethod
    def create_new(
        name: str,
        description: str,
        image_id: str,
        owner_account_id: str,
        start_date: date,
        end_date: date,
        additional_links: list[EventAdditionalLink],
        participant_ids: list[str]
    ):
        return Event(
            id_=str(uuid4()).lower(),
            name=name,
            description=description,
            image_id=image_id,
            owner_account_id=owner_account_id,
            start_date=start_date,
            end_date=end_date,
            additional_links=additional_links,
            participant_ids=participant_ids
        )

    def update(
        self,
        name: str,
        description: str,
        image_id: str,
        start_date: date,
        end_date: date,
        additional_links: list[EventAdditionalLink],
        participants: list[EventParticipant]
    ):
        self.name = name
        self.description = description
        self.image_id = image_id
        self.start_date = start_date
        self.end_date = end_date
        self.additional_links = additional_links
        self.participants = participants
