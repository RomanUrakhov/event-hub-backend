from application.interfaces.repositories.account import IUserAccountRepository

from sqlalchemy.orm import Session

from domain.models.account import UserAccount


class MySQLUserAccountRepository(IUserAccountRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_external_id(self, external_id: str) -> UserAccount:
        return (
            self._session.query(UserAccount)
            .filter(UserAccount.twitch_id == external_id)
            .first()
        )

    def create_account(self, account: UserAccount) -> None:
        self._session.add(account)
        self._session.commit()
