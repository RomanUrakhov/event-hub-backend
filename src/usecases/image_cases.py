import uuid

from src.services.file_manager import IFileManager


def upload_image(file: bytes, file_manager: IFileManager):
    file_id = str(uuid.uuid4()).lower()
    file_manager.save(file, file_id)
    return file_id


def get_image(file_id: str, file_manager: IFileManager) -> bytes:
    return file_manager.get(file_id)
