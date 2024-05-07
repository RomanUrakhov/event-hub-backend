from abc import ABC, abstractmethod

from src.domain.event import Event


class EventNotFound(Exception):
    pass


class IEventRepository(ABC):
    @abstractmethod
    def create_event(self, event: Event) -> None:
        pass

    @abstractmethod
    def update_event(self, event: Event) -> None:
        pass

    @abstractmethod
    def get_by_id(self, event_id: str) -> Event:
        pass

    @abstractmethod
    def get_all(self) -> list[Event]:
        pass


class FakeSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(FakeSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class FakeEventRepository(IEventRepository):
    __metaclass__ = FakeSingleton

    def __init__(self, events: list[Event]):
        self.events = events

    def create_event(self, event: Event) -> None:
        self.events.append(event)

    def get_by_id(self, event_id: str) -> Event:
        for event in self.events:
            if event.id_ == event_id:
                return event
        raise Exception(f'Event with id {event_id} not found')

    def update_event(self, event: Event) -> None:
        for i, event_ in enumerate(self.events):
            if event_.id_ == event.id_:
                self.events[i] = event
                return
        raise Exception(f'Event with id {event.id_} not found')

    def get_all(self) -> list[Event]:
        return self.events
