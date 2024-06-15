class StreamerNotExistsException(Exception):
    def __init__(self, streamer_id: str) -> None:
        self.streamer_id = streamer_id
        super().__init__(f"streamer not found for ID: {streamer_id}")
