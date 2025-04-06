from application.use_cases.dto.auth import LoginAccountResult, User
from common.helpers import ulid_from_datetime_utc
from domain.models.account import UserAccount
from src.application.interfaces.repositories.account import IUserAccountRepository
from src.infrastructure.services.auth import AuthPayload, IAuthProvider


class AccountNotFoundException(Exception):
    pass


def _create_login_response(
    auth_data: AuthPayload, user_account: UserAccount
) -> LoginAccountResult:
    return LoginAccountResult(
        id_token=auth_data.access_token,
        refresh_token=auth_data.refresh_token,
        user=User(
            id=user_account.id,
            name=auth_data.user_payload.name,
            avatar=auth_data.user_payload.avatar,
        ),
    )


def login_account(
    auth_code: str,
    auth_provider: IAuthProvider,
    user_account_repo: IUserAccountRepository,
) -> LoginAccountResult:
    auth_data = auth_provider.authenticate_user(auth_code)

    user_account = user_account_repo.get_by_external_id(
        auth_data.user_payload.external_id
    )
    if user_account:
        return _create_login_response(auth_data, user_account)
    new_user_account = UserAccount(
        id=ulid_from_datetime_utc(), twitch_id=auth_data.user_payload.external_id
    )
    user_account_repo.create_account(new_user_account)

    return _create_login_response(auth_data, new_user_account)
