from src.application.interfaces.services.file_manager import IFileManager


class OSFileManager(IFileManager):

    def __init__(self, root_dir: str):
        self.root_dir = root_dir

    def save(self, file: bytes, file_id: str) -> None:
        pass

    def get(self, file_id: str) -> bytes:
        pass


class FakeFileManager(IFileManager):
    def __init__(self):
        self.files = {}

    def save(self, file: bytes, file_id: str) -> None:
        self.files[file_id] = file

    def get(self, file_id: str) -> bytes:
        return self.files[file_id]
