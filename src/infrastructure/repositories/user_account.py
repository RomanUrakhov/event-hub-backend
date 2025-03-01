from application.interfaces.repositories.account import (
    IAccountAppAccessRepository,
    IAccountEventAccessRepository,
    IUserAccountRepository,
)

from sqlalchemy.orm import Session

from domain.models.account import AccountAppAccess, AccountEventAccess, UserAccount


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


class MySQLAccountEventAccessRepository(IAccountEventAccessRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_account_access(
        self, account_id: str, event_id: str
    ) -> AccountEventAccess | None:
        return (
            self._session.query(AccountEventAccess)
            .filter(
                AccountEventAccess.account_id == account_id,
                AccountEventAccess.event_id == event_id,
            )
            .one_or_none()
        )


class MySQLAccountAppAccessRepository(IAccountAppAccessRepository):
    def __init__(self, session: Session):
        self._session = session

    def account_has_global_access(self, account_id: str) -> bool:
        """Check if a user has a record in account_app_access (meaning they have global admin access)."""
        return (
            self._session.query(AccountAppAccess)
            .filter(AccountAppAccess.account_id == account_id)
            .one_or_none()
            is not None
        )
