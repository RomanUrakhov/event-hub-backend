from abc import ABC, abstractmethod

from domain.models.event import Event


class IEventRepository(ABC):
    @abstractmethod
    def check_exists(self, event_id: str) -> bool:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Event | None:
        pass

    @abstractmethod
    def get_by_slug(self, slug: str) -> Event | None:
        pass

    @abstractmethod
    def create(self, event: Event):
        pass

    @abstractmethod
    def update(self, event: Event):
        pass
