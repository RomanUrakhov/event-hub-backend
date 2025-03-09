from typing import Optional
from application.interfaces.dao.streamer import (
    IStreamerDAO,
    StreamerDetailsDTO,
    StreamerEventItem,
)
from domain.models.participation import Participation
from domain.models.streamer import Streamer
from domain.models.event import Event

from sqlalchemy.orm import Session
from sqlalchemy.orm import load_only


class InMemoryStreamerDAO(IStreamerDAO):
    def __init__(self, data: list[StreamerDetailsDTO]) -> None:
        self._data = data

    def get_streamer_details(self, streamer_id) -> Optional[StreamerDetailsDTO]:
        streamer = next((s for s in self._data if s.id == streamer_id), None)
        return streamer


class MySQLStreamerDAO(IStreamerDAO):
    def __init__(self, session: Session):
        self.session = session

    def get_streamer_details(self, streamer_id: str) -> StreamerDetailsDTO | None:
        streamer = self.session.query(Streamer).filter_by(id=streamer_id).one_or_none()
        if not streamer:
            return None

        query = (
            self.session.query(Event)
            .join(Participation, Participation.event_id == Event.id)
            .filter(Participation.streamer_id == streamer_id)
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

        events = [
            StreamerEventItem(
                id=event.id,
                name=event.name,
                start_date=event.start_date,
                end_date=event.end_date,
                image_id=event.image_id,
            )
            for event in query
        ]

        return StreamerDetailsDTO(
            id=streamer.id,
            twitch_id=streamer.twitch_id,
            name=streamer.name,
            events=events,
        )
