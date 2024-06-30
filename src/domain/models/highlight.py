from datetime import datetime

from common.helpers import current_datetime_utc


from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from domain import Base


class Highlight(Base):
    __tablename__ = "highlight"

    url: Mapped[str] = mapped_column(String, primary_key=True)
    author_id: Mapped[str] = mapped_column(
        ForeignKey("user_accounts.id"), nullable=False
    )
    event_id: Mapped[str] = mapped_column(ForeignKey("event.id"), nullable=False)
    attached_datetime: Mapped[datetime] = mapped_column(
        DateTime, default=current_datetime_utc
    )

    def __eq__(self, other: "Highlight") -> bool:
        if isinstance(other, Highlight):
            return self.url == other.url
        return False
