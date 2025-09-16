from application.interfaces.repositories.participation import IParticipationRepository
from domain.models.participation import Participation

from infrastructure.repositories.base import BaseSQLAlchemyRepository


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


class MySQLParticipationRepository(BaseSQLAlchemyRepository, IParticipationRepository):
    def check_exists(self, event_id: str, streamer_id: str) -> bool:
        return (
            self._session.query(Participation)
            .filter_by(event_id=event_id, streamer_id=streamer_id)
            .first()
            is not None
        )

    def save(self, participation: Participation):
        self._session.add(participation)
        self._session.commit()

    def save_batch(self, participations: list[Participation]):
        self._session.bulk_save_objects(participations)
        self._session.commit()
