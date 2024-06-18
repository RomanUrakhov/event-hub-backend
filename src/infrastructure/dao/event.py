from datetime import date
from application.interfaces.dao.event import (
    EventDetailsDTO,
    EventListItemDTO,
    IEventDAO,
)
from domain.models.event import EventAdditionalLink


class InMemoryEventDAO(IEventDAO):
    def __init__(self):
        self._detailed_event = EventDetailsDTO(
            id="123",
            name="123",
            image_id="123",
            description="123",
            start_date=date.fromisoformat("2024-05-01"),
            end_date=date.fromisoformat("2024-05-10"),
            additional_links=[
                EventAdditionalLink(url="https://www.twitch.tv/", name="123")
            ],
        )
        self._list_events = [
            EventListItemDTO(
                id="123",
                name="123",
                image_id="123",
                start_date=date.fromisoformat("2024-05-01"),
                end_date=date.fromisoformat("2024-05-10"),
            ),
            EventListItemDTO(
                id="456",
                name="456",
                image_id="456",
                start_date=date.fromisoformat("2024-06-01"),
                end_date=date.fromisoformat("2024-06-10"),
            ),
        ]

    def get_event(self, id: str) -> EventDetailsDTO:
        return self._detailed_event

    def list_events(self) -> list[EventListItemDTO]:
        return self._list_events
