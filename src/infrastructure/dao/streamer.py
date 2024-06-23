from typing import Optional
from application.interfaces.dao.streamer import (
    IStreamerDAO,
    StreamerDetailsDTO,
)


class InMemoryStreamerDAO(IStreamerDAO):
    def __init__(self, data: list[StreamerDetailsDTO]) -> None:
        self._data = data

    def get_streamer_details(self, streamer_id) -> Optional[StreamerDetailsDTO]:
        streamer = next((s for s in self._data if s.id == streamer_id), None)
        return streamer
