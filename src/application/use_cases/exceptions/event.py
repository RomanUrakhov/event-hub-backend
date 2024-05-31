class EventNotFoundException(Exception):
    def __init__(self, event_id) -> None:
        self.event_id = event_id
        super().__init__(f"Event not found for ID: {event_id}")
