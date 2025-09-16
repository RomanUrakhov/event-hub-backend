from application.interfaces.repositories.account import (
    IAccountAppAccessRepository,
    IAccountEventAccessRepository,
    IUserAccountRepository,
)

from domain.models.account import AccountAppAccess, AccountEventAccess, UserAccount
from infrastructure.repositories.base import BaseSQLAlchemyRepository


class MySQLUserAccountRepository(BaseSQLAlchemyRepository, IUserAccountRepository):
    def get_by_external_id(self, external_id: str):
        return (
            self._session.query(UserAccount)
            .filter(UserAccount.twitch_id == external_id)
            .first()
        )

    def create_account(self, account: UserAccount):
        self._session.add(account)
        self._session.commit()


class MySQLAccountEventAccessRepository(
    BaseSQLAlchemyRepository, IAccountEventAccessRepository
):
    def get_account_access(self, account_id: str, event_id: str):
        return (
            self._session.query(AccountEventAccess)
            .filter(
                AccountEventAccess.account_id == account_id,
                AccountEventAccess.event_id == event_id,
            )
            .one_or_none()
        )

    def list_account_accesses(self, account_id: str):
        return (
            self._session.query(AccountEventAccess)
            .filter(AccountEventAccess.account_id == account_id)
            .all()
        )


class MySQLAccountAppAccessRepository(
    BaseSQLAlchemyRepository, IAccountAppAccessRepository
):
    def account_has_global_access(self, account_id: str):
        """Check if a user has a record in account_app_access (meaning they have global admin access)."""
        return (
            self._session.query(AccountAppAccess)
            .filter(AccountAppAccess.account_id == account_id)
            .one_or_none()
            is not None
        )
