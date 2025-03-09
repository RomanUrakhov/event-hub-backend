from sqlalchemy.orm import Session, load_only

from datetime import date
from application.interfaces.dao.event import (
    EventDetailsAdditionalLinkDTO,
    EventDetailsDTO,
    EventDetailsHighlightDTO,
    EventListItemDTO,
    IEventDAO,
)
from domain.models.event import Event, EventAdditionalLink
from domain.models.highlight import Highlight


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
            highlights=[
                Highlight(url="https://www.twitch.tv/dota2_paragon_ru", author_id="123")
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

    def get_event(self, id: str) -> EventDetailsDTO | None:
        return self._detailed_event

    def list_events(self) -> list[EventListItemDTO]:
        return self._list_events


class MySQLEventDAO(IEventDAO):
    def __init__(self, session: Session):
        self.session = session

    def get_event(self, id: str) -> EventDetailsDTO | None:
        event_query = self.session.query(Event).filter_by(id=id).one_or_none()

        if not event_query:
            return None

        hl_dtos = [
            EventDetailsHighlightDTO(
                author_id=highlight.author_id,
                url=highlight.url,
                attached_datetime=highlight.attached_datetime,
            )
            for highlight in event_query.highlights
        ]

        additional_links_dtos = [
            EventDetailsAdditionalLinkDTO(url=l.url, name=l.name)
            for l in event_query.additional_links
        ]

        detailed_event = EventDetailsDTO(
            id=event_query.id,
            name=event_query.name,
            start_date=event_query.start_date,
            end_date=event_query.end_date,
            image_id=event_query.image_id,
            description=event_query.description,
            additional_links=additional_links_dtos,
            highlights=hl_dtos,
        )

        return detailed_event

    def list_events(self) -> list[EventListItemDTO]:
        events_query = (
            self.session.query(Event)
            .options(
                load_only(
                    Event.id,
                    Event.name,
                    Event.start_date,
                    Event.end_date,
                    Event.image_id,
                )
            )
            .all()
        )

        list_events = [
            EventListItemDTO(
                id=event.id,
                name=event.name,
                start_date=event.start_date,
                end_date=event.end_date,
                image_id=event.image_id,
            )
            for event in events_query
        ]

        return list_events
