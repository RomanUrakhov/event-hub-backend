from functools import wraps
from flask import g, request
from apiflask import abort, APIBlueprint

from api.schemas.auth import AuthWithTwitchRequestSchema, AuthWithTwitchResponseSchema
from application.interfaces.services.auth import AuthException, IAuthProvider
from src.application.interfaces.repositories.account import IUserAccountRepository
from src.application.use_cases.auth import login_account


# TODO: maybe rewrite to Flask-HTTPAuth
def token_required(
    auth_provider: IAuthProvider, account_repository: IUserAccountRepository
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                return abort(401)

            id_token = auth_header.split(" ", 1)[1]

            if not id_token:
                return abort(401)

            # TODO: distinguish between different types of error (e.g. "Id Token Expired", etc.)
            try:
                user_payload = auth_provider.validate_token(id_token)
            except AuthException:
                return abort(401)
            account = account_repository.get_by_external_id(user_payload.external_id)

            g.user_account = account

            return func(*args, **kwargs)

        return wrapper

    return decorator


def create_auth_blueprint(
    auth_provider: IAuthProvider, account_repository: IUserAccountRepository
):
    bp = APIBlueprint("auth", __name__)

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
            )
        except AuthException as e:
            abort(
                400,
                message=str(e),
            )

        return login_response.model_dump()

    return bp
