from abc import ABC, abstractmethod

from src.domain.models.event import Event


class IEventRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: str) -> Event | None:
        pass

    @abstractmethod
    def get_by_slug(self, slug: str) -> Event | None:
        pass

    @abstractmethod
    def create(self, event: Event) -> None:
        pass
