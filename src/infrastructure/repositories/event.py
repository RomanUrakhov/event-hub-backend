from src.application.interfaces.repositories.event import IEventRepository
from src.domain.models.event import Event


class InMemoryEventRepository(IEventRepository):
    def __init__(self, events: list[Event] = None):
        self._events = events or []

    def check_exists(self, event_id: str) -> bool:
        return True

    def get_by_id(self, id: str) -> Event | None:
        return next((e for e in self._events if e.id == id), None)

    def get_by_slug(self, slug: str) -> Event | None:
        return next((e for e in self._events if e.slug == slug), None)

    def create(self, event: Event) -> None:
        return self._events.append(event)

    def update(self, event: Event):
        return
