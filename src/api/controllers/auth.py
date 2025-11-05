from functools import wraps
from flask import current_app, g, request
from apiflask import abort, APIBlueprint
import jwt

from api.schemas.auth import (
    AuthWithTwitchRequestSchema,
    AuthWithTwitchResponseSchema,
    RefreshTokenResponseSchema,
)
from application.interfaces.services.auth import AuthException, IAuthProvider
from src.application.interfaces.repositories.account import IUserAccountRepository
from src.application.use_cases.auth import (
    RefreshTokenError,
    login_account,
    refresh_user_session,
)


# TODO: maybe rewrite to Flask-HTTPAuth
def token_required(
    account_repository: IUserAccountRepository, verify_expiration: bool = True
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                return abort(401, "Authorization header is missing or invalid")

            id_token = auth_header.split(" ", 1)[1]

            try:
                decode_options = {"verify_exp": verify_expiration}
                payload = jwt.decode(
                    id_token,
                    current_app.config["JWT_SECRET_KEY"],
                    algorithms=["HS256"],
                    options=decode_options,
                )

                user_id = payload["sub"]
                account = account_repository.get_by_id(user_id)
                if not account:
                    abort(401, "Token is invalid.")

                g.user_account = account
                g.session_token = id_token

            except jwt.ExpiredSignatureError:
                abort(401, "Token has expired")
            except jwt.InvalidTokenError:
                abort(401, "Token is invalid")

            return func(*args, **kwargs)

        return wrapper

    return decorator


def create_auth_blueprint(
    auth_provider: IAuthProvider,
    account_repository: IUserAccountRepository,
    secret_key: str,
):
    bp = APIBlueprint("auth", __name__)

    refresh_auth = token_required(account_repository, verify_expiration=False)

    @bp.route("/auth/twitch", methods=["POST"])
    @bp.input(AuthWithTwitchRequestSchema)
    @bp.output(AuthWithTwitchResponseSchema)
    @bp.doc(
        operation_id="authWithTwitch",
        responses={"400": {"description": "Twitch authentication flow failed"}},
    )
    def twitch_auth(json_data):
        code = json_data.get("code")

        try:
            login_response = login_account(
                auth_code=code,
                auth_provider=auth_provider,
                user_account_repo=account_repository,
                secret_key=secret_key,
            )
        except AuthException as e:
            abort(
                400,
                message=str(e),
            )

        return login_response.model_dump()

    @bp.route("/auth/refresh", methods=["POST"])
    @bp.output(RefreshTokenResponseSchema)
    @refresh_auth
    @bp.doc(
        operation_id="refreshToken",
        responses={"401": {"description": "Refresh failed or token is invalid"}},
        security=[{"InternalBearerAuth": []}],
    )
    def refresh_session():
        token = g.session_token

        try:
            new_session_token = refresh_user_session(
                token, secret_key, account_repository
            )

            return {"session_token": new_session_token}
        except RefreshTokenError as e:
            abort(401, str(e))

    return bp
