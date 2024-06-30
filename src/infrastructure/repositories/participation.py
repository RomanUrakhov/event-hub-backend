from application.interfaces.repositories.participation import IParticipationRepository
from domain.models.participation import Participation

from sqlalchemy.orm import Session


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


class MySQLParticipationRepository(IParticipationRepository):
    def __init__(self, session: Session):
        self.session = session

    def check_exists(self, event_id: str, streamer_id: str) -> bool:
        return (
            self.session.query(Participation)
            .filter_by(event_id=event_id, streamer_id=streamer_id)
            .first()
            is not None
        )

    def save(self, participation: Participation):
        self.session.add(participation)
        self.session.commit()

    def save_batch(self, participations: list[Participation]):
        self.session.bulk_save_objects(participations)
        self.session.commit()
