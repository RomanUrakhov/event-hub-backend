from application.use_cases.dto.streamer import CreateStreamerCommand
from application.interfaces.repositories.streamer import IStreamerRepository
from common.helpers import ulid_from_datetime_utc
from domain.exceptions.streamer import StreamerAlreadyExistsException
from domain.models.streamer import Streamer


class CreateStreamer:
    def __init__(self, streamer_repository: IStreamerRepository):
        self._streamer_repo = streamer_repository

    def __call__(self, command: CreateStreamerCommand):
        streamer = self._streamer_repo.get_by_twitch_id(command.twitch_id)

        if streamer:
            raise StreamerAlreadyExistsException(streamer.id, command.twitch_id)

        streamer = Streamer(
            id=ulid_from_datetime_utc(), name=command.name, twitch_id=command.twitch_id
        )

        self._streamer_repo.create(streamer)

        return streamer.id
