from abc import ABC, abstractmethod

from domain.models.participation import Participation


class IParticipationRepository(ABC):
    @abstractmethod
    def check_exists(self, event_id: str, streamer_id: str) -> bool:
        pass

    @abstractmethod
    def save(self, participation: Participation):
        pass

    @abstractmethod
    def save_batch(self, participations: list[Participation]):
        pass
