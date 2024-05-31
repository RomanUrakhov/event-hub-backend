from src.application.interfaces.repositories.event import IEventRepository
from src.domain.models.event import Event


class InMemoryEventRepository(IEventRepository):
    def __init__(self, events: list[Event] = None):
        self._events = events or []

    def get_by_id(self, id: str) -> Event | None:
        return next((e for e in self._events if e.id == id), None)
