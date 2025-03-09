from application.interfaces.repositories.event import IEventRepository
from domain.models.event import Event

from sqlalchemy.orm import Session


class InMemoryEventRepository(IEventRepository):
    def __init__(self, events: list[Event] | None = None):
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


class MySQLEventRepository(IEventRepository):
    def __init__(self, session: Session):
        self._session = session

    def check_exists(self, event_id: str) -> bool:
        return self._session.query(Event).filter_by(id=event_id).first() is not None

    def get_by_id(self, id: str) -> Event | None:
        return self._session.query(Event).filter_by(id=id).one_or_none()

    def get_by_slug(self, slug: str) -> Event | None:
        return self._session.query(Event).filter_by(slug=slug).one_or_none()

    def create(self, event: Event) -> None:
        self._session.add(event)
        self._session.commit()

    def update(self, event: Event):
        self._session.merge(event)
        self._session.commit()
