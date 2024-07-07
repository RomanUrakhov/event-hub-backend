from abc import ABC, abstractmethod


class IUserAccountRepository(ABC):
    @abstractmethod
    def get_by_external_id(self, id: str):
        pass

    @abstractmethod
    def create_account(self, data: dict):
        pass
