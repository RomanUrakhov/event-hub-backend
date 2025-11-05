from abc import ABC, abstractmethod

from domain.models.account import AccountEventAccess, UserAccount


class IUserAccountRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: str) -> UserAccount | None:
        pass

    @abstractmethod
    def get_by_external_id(self, id: str) -> UserAccount | None:
        pass

    @abstractmethod
    def save(self, account: UserAccount):
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
