from datetime import datetime, timedelta, timezone

import jwt
from application.use_cases.dto.auth import LoginAccountResult, User
from common.helpers import ulid_from_datetime_utc
from domain.models.account import UserAccount
from src.application.interfaces.repositories.account import IUserAccountRepository
from src.infrastructure.services.auth import AuthPayload, IAuthProvider


class AccountNotFoundException(Exception):
    pass


def _create_session_token(user_id: str, secret_key: str) -> str:
    """Generates the internal session JWT"""
    session_token_payload = {
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
        "sub": user_id,
    }
    return jwt.encode(session_token_payload, secret_key, algorithm="HS256")


def _create_login_response(
    auth_data: AuthPayload, user_account: UserAccount, secret_key: str
) -> LoginAccountResult:
    session_token = _create_session_token(user_account.id, secret_key)

    return LoginAccountResult(
        session_token=session_token,
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
    secret_key: str,
) -> LoginAccountResult:
    auth_data = auth_provider.authenticate_user(auth_code)

    user_account = user_account_repo.get_by_external_id(
        auth_data.user_payload.external_id
    )

    if not user_account:
        user_account = UserAccount(
            id=ulid_from_datetime_utc(),  # type: ignore
            twitch_id=auth_data.user_payload.external_id,  # type: ignore
        )
        user_account_repo.save(user_account)

    return _create_login_response(auth_data, user_account, secret_key)


class RefreshTokenError(Exception):
    pass


def refresh_user_session(
    expired_token: str,
    secret_key: str,
    account_repository: IUserAccountRepository,
) -> str:
    try:
        payload = jwt.decode(
            expired_token,
            secret_key,
            algorithms=["HS256"],
            options={"verify_exp": False},
        )
        user_id = payload["sub"]
        account = account_repository.get_by_id(user_id)

        if not account:
            raise RefreshTokenError("Invalid token: user not found.")

        return _create_session_token(user_id, secret_key)

    except jwt.InvalidTokenError as e:
        raise RefreshTokenError("Failed to refresh token: token is invalid.") from e
