from abc import ABC, abstractmethod


class IAccountRepository(ABC):
    @abstractmethod
    def get_by_external_id(id: str):
        pass

    @abstractmethod
    def create_account(data: dict):
        pass
