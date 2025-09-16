from abc import ABC, abstractmethod
from typing import Optional

from infrastructure.dto.twitch_dto import TwitchUserDTO


class ITwitchService(ABC):
    @abstractmethod
    def get_user_by_id(self, twitch_id: str) -> Optional[TwitchUserDTO]:
        """Fetch Twitch user info by Twitch ID."""
        pass

    @abstractmethod
    def list_users_by_ids(self, twitch_ids: list[str]) -> list[TwitchUserDTO]:
        """Fetch list of Twitch users info by their Twitch IDs"""
        pass
