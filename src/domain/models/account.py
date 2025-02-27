from enum import Enum

from domain import Base

from sqlalchemy import ForeignKey, Integer, String, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserAccount(Base):
    __tablename__ = "user_account"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    twitch_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)


class RoleName(Enum):
    ADMIN = "Admin"
    MODERATOR = "Moderator"
    PARTICIPANT = "Participant"


class EventRole(Base):
    __tablename__ = "event_role"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[RoleName] = mapped_column(
        SqlEnum(
            RoleName,
            values_callable=lambda enum_class: [member.value for member in enum_class],
        ),
        nullable=False,
    )


class AccountEventAccess(Base):
    __tablename__ = "account_event_access"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    account_id: Mapped[str] = mapped_column(
        ForeignKey("user_account.id"), nullable=False
    )
    role_id: Mapped[str] = mapped_column(ForeignKey("event_role.id"), nullable=False)
    event_id: Mapped[str] = mapped_column(ForeignKey("event.id"), nullable=False)

    role: Mapped["EventRole"] = relationship("EventRole")

    def can_enroll_streamers_on_event(self) -> bool:
        return self.role.name == RoleName.ADMIN

    def can_moderate_highlights_on_event(self) -> bool:
        return self.role.name in (RoleName.ADMIN, RoleName.MODERATOR)
