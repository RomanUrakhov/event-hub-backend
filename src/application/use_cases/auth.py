from typing import NamedTuple

from common.helpers import ulid_from_datetime_utc
from domain.models.account import UserAccount
from src.application.interfaces.repositories.account import IUserAccountRepository
from src.infrastructure.services.auth import AuthPayload, IAuthProvider


class LoginAccountResponse(NamedTuple):
    id_token: str
    refresh_token: str
    user_avatar: str
    user_name: str
    user_id: str


class AccountNotFoundException(Exception):
    pass


def _create_login_response(
    auth_data: AuthPayload, user_account: UserAccount
) -> LoginAccountResponse:
    return LoginAccountResponse(
        id_token=auth_data.access_token,
        refresh_token=auth_data.refresh_token,
        user_avatar=auth_data.user_payload.avatar,
        user_name=auth_data.user_payload.name,
        user_id=user_account.id,
    )


def login_account(
    auth_code: str,
    auth_provider: IAuthProvider,
    user_account_repo: IUserAccountRepository,
) -> LoginAccountResponse:
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


# def has_system_access(
#     user_id: str, user_account_repository: IUserAccountRepository
# ) -> bool:
#     user = user_account_repository.get_by_id(user_id)
#     return user.can_create_event()


# def has_event_access(
#     user_id: str,
#     event_id: str,
#     action: SpecificEventAction,
#     user_account_repository: IUserAccountRepository,
# ) -> bool:
#     user = user_account_repository.get_by_id(user_id)
#     return user.can_perform_action_on_event(event_id, action)
