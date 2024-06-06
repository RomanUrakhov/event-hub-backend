from abc import ABC, abstractmethod


class IFileManager(ABC):
    @abstractmethod
    def save(self, file: bytes, file_id: str) -> None:
        pass

    @abstractmethod
    def get(self, file_id: str) -> bytes:
        pass
