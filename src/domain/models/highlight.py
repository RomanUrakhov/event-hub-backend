from dataclasses import dataclass, field
from datetime import datetime

from pydantic import Field

from common.helpers import current_datetime_utc


@dataclass
class Highlight:
    url: str = field()
    author_id: str
    attached_datetime: datetime = Field(default_factory=current_datetime_utc)

    def __eq__(self, other: "Highlight") -> bool:
        if isinstance(other, Highlight):
            return self.url == other.url
        return False
