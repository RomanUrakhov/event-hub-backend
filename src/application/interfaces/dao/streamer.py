from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date


# TODO: standardize DAO methods' names
# (e.g. here 'get_streamer_details', but for event there's 'get_event')


@dataclass
class StreamerEventItem:
    id: str
    name: str
    start_date: date
    end_date: date
    image_id: str


@dataclass
class StreamerDetailsDTO:
    id: str
    twitch_id: str
    name: str

    events: list[StreamerEventItem] = field(default_factory=list)


class IStreamerDAO(ABC):
    @abstractmethod
    def get_streamer_details(self, streamer_id) -> StreamerDetailsDTO:
        pass
