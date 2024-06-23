from application.interfaces.repositories.participation import IParticipationRepository
from domain.models.participation import Participation


class InMemoryParticipationRepository(IParticipationRepository):
    def __init__(self, participations: list[Participation]):
        self._participations = participations

    def check_exists(self, event_id: str, streamer_id: str) -> bool:
        participation = next(
            (
                p
                for p in self._participations
                if p.event_id == event_id and p.streamer_id == streamer_id
            ),
            None,
        )
        return participation is not None

    def save(self, participation: Participation):
        self._participations.append(participation)

    def save_batch(self, participations: list[Participation]):
        self._participations.extend(participations)
