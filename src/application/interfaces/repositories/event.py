from abc import ABC, abstractmethod

from src.domain.models.event import Event


class IEventRepository(ABC):
    @abstractmethod
    def get_by_id(id: str) -> Event | None:
        pass
