from dataclasses import dataclass, field


@dataclass
class Participation:
    id: str
    event_id: str
    streamer_id: str
    is_winner: bool = field(default=False)

    # TODO: Where to put logic of checking that event can have only one winner?
