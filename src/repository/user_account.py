from abc import ABC, abstractmethod

from src.domain.user_account import UserAccount


class AccountAlreadyExists(Exception):
    pass


class AccountNotFoundException(Exception):
    pass


class IUserAccountRepository(ABC):
    @abstractmethod
    def create_account(self, user_account: UserAccount):
        pass

    @abstractmethod
    def get_by_external_id(self, external_user_id: str) -> UserAccount:
        pass

    @abstractmethod
    def get_by_id(self, id_: str) -> UserAccount:
        pass


class FakeUserAccountRepository(IUserAccountRepository):
    def __init__(self):
        self.accounts = []

    def create_account(self, user_account: UserAccount):
        self.accounts.append(user_account)

    def get_by_external_id(self, external_user_id: str) -> UserAccount:
        return next((account for account in self.accounts if account.external_user_id == external_user_id), None)

    def get_by_id(self, id_: str) -> UserAccount:
        return next((account for account in self.accounts if account.id_ == id_), None)
