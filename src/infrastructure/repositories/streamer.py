from typing import Optional
from application.interfaces.repositories.streamer import IStreamerRepository
from domain.models.streamer import Streamer


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
