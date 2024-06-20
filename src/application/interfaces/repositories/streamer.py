from abc import ABC, abstractmethod

from domain.models.streamer import Streamer


class IStreamerRepository(ABC):
    @abstractmethod
    def check_exists(self, streamer_id: str) -> bool:
        pass

    @abstractmethod
    def get_by_twitch_id(self, twitch_id: str) -> Streamer:
        pass

    @abstractmethod
    def list_by_ids(self, streamer_ids: list[str]) -> list[Streamer]:
        pass
