class ParticipationAlreadyExists(Exception):
    def __init__(self, event_id: str, streamer_id: str) -> None:
        self.event_id = event_id
        self.streamer_id = streamer_id
        super().__init__(
            f"Participation already exists: (event_id:{self.event_id}, streamer_id:{self.streamer_id}"
        )
