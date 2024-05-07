from uuid import uuid4

from datetime import datetime
from enum import Enum


class SystemRole(Enum):
    ADMIN = 0
    STREAMER = 1
    COMMON_USER = 2


class EventRole(Enum):
    OWNER = 0
    MODERATOR = 1
    HIGHLIGHTER = 2


class SpecificEventAction(Enum):
    UPDATE_METADATA = 'update_metadata'
    HIGHLIGHT_MODERATION = 'highlight_moderation'
    DELETE_EVENT = 'delete_event'


class EventAccess:
    def __init__(
        self,
        event_id: str,
        role: EventRole,
        grant_author_account: "UserAccount",
        granted_at: datetime
    ):
        self.event_id = event_id
        self.role = role
        self.grant_author_account = grant_author_account
        self.granted_at = granted_at

    def __eq__(self, other: "EventAccess"):
        if not isinstance(other, EventAccess):
            return NotImplemented
        return self.event_id == other.event_id and self.role == other.role

    def _is_update_allowed(self) -> bool:
        return self.role in [EventRole.OWNER, EventRole.MODERATOR]

    def _is_highlight_moderation_allowed(self) -> bool:
        return self.role in [EventRole.OWNER, EventRole.MODERATOR, EventRole.HIGHLIGHTER]

    def _is_delete_allowed(self) -> bool:
        return self.role == EventRole.OWNER

    def is_allowed(self, action: SpecificEventAction) -> bool:
        __checkers = {
            SpecificEventAction.UPDATE_METADATA: self._is_update_allowed,
            SpecificEventAction.HIGHLIGHT_MODERATION: self._is_highlight_moderation_allowed,
            SpecificEventAction.DELETE_EVENT: self._is_delete_allowed
        }
        return __checkers[action]()


class UserAccount:
    def __init__(
        self,
        id_: str,
        external_user_id: str,
        accesses: list[EventAccess] = None,
        system_role: SystemRole = SystemRole.COMMON_USER
    ):
        self.id_ = id_
        self.external_user_id = external_user_id
        self.accesses = accesses or []
        self.system_role = system_role

    @staticmethod
    def create_new(external_user_id: str):
        return UserAccount(
            id_=str(uuid4()).lower(),
            external_user_id=external_user_id
        )

    def can_create_event(self) -> bool:
        return self.system_role in [SystemRole.ADMIN, SystemRole.STREAMER]

    def _access_to_event(self, event_id: str) -> EventAccess:
        return next((access for access in self.accesses if access.event_id == event_id), None)

    def can_perform_action_on_event(self, event_id: str, action: SpecificEventAction) -> bool:
        access = self._access_to_event(event_id)
        if self.system_role == SystemRole.ADMIN or (access and access.is_allowed(action)):
            return True
        return False
