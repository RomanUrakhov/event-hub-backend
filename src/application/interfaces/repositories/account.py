from abc import ABC, abstractmethod

from domain.models.account import AccountEventAccess, UserAccount


class IUserAccountRepository(ABC):
    @abstractmethod
    def get_by_external_id(self, id: str) -> UserAccount:
        pass

    @abstractmethod
    def create_account(self, data: dict):
        pass


class IAccountEventAccessRepository(ABC):
    @abstractmethod
    def get_account_access(
        self, account_id: str, event_id: str
    ) -> AccountEventAccess | None:
        pass

    @abstractmethod
    def list_account_accesses(self, account_id: str) -> list[AccountEventAccess]:
        pass


class IAccountAppAccessRepository(ABC):
    @abstractmethod
    def account_has_global_access(self, account_id: str) -> bool:
        pass
