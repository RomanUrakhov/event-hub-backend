class StreamerNotExistsException(Exception):
    def __init__(self, streamer_id: str) -> None:
        self.streamer_id = streamer_id
        super().__init__(f"streamer not found for ID: {streamer_id}")


class StreamerAlreadyExistsException(Exception):
    def __init__(self, streamer_id: str, twitch_id: str):
        super().__init__(
            f"streamer with such twitch id already exists (twitch_id: {twitch_id}, internal_id: {streamer_id})"
        )
