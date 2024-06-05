class EventNotFoundException(Exception):
    def __init__(self, event_id) -> None:
        self.event_id = event_id
        super().__init__(f"Event not found for ID: {event_id}")


class EventAlreadyExistsException(Exception):
    def __init__(self, event_name: str) -> None:
        self.event_name = event_name
        super().__init__(f"Event with such name already exists: {event_name}")
