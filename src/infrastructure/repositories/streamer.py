from typing import Optional
from application.interfaces.repositories.streamer import IStreamerRepository
from domain.models.streamer import Streamer


from sqlalchemy.orm import Session


class InMemoryStreamerRepository(IStreamerRepository):
    def __init__(self, streamers: list[Streamer]):
        self._streamers = streamers

    def check_exists(self, streamer_id: str) -> bool:
        streamer = next((s for s in self._streamers if s.id == streamer_id), None)
        return streamer is not None

    def get_by_twitch_id(self, twitch_id: str) -> Optional[Streamer]:
        streamer = next((s for s in self._streamers if s.twitch_id == twitch_id), None)
        return streamer

    def list_by_ids(self, streamer_ids: list[str]) -> list[Streamer]:
        return [s for s in self._streamers if s.id in streamer_ids]

    def create(self, streamer: Streamer):
        return self._streamers.append(streamer)


class MySQLStreamerRepository(IStreamerRepository):
    def __init__(self, session: Session):
        self._session = session

    def check_exists(self, streamer_id: str) -> bool:
        return (
            self._session.query(Streamer).filter_by(id=streamer_id).first() is not None
        )

    def get_by_twitch_id(self, twitch_id: str) -> Streamer:
        return (
            self._session.query(Streamer).filter_by(twitch_id=twitch_id).one_or_none()
        )

    def list_by_ids(self, streamer_ids: list[str]) -> list[Streamer]:
        return self._session.query(Streamer).filter(Streamer.id.in_(streamer_ids)).all()

    def create(self, streamer: Streamer):
        self._session.add(streamer)
        self._session.commit()
