from functools import wraps
from flask import Blueprint, g, jsonify, request

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
            id_token = request.cookies.get("id_token")

            if not id_token:
                return jsonify({"error": "Unauthorized"}), 401

            # TODO: distinguish between different types of error (e.g. "Id Token Expired", etc.)
            try:
                user_payload = auth_provider.validate_token(id_token)
            except AuthException:
                return jsonify({"error": "Unauthorized"}), 401

            account = account_repository.get_by_external_id(user_payload.external_id)

            g.user_account = account

            return func(*args, **kwargs)

        return wrapper

    return decorator


def create_auth_blueprint(
    auth_provider: IAuthProvider, account_repository: IUserAccountRepository
):
    bp = Blueprint("auth", __name__)

    @bp.route("/auth/twitch", methods=["POST"])
    def twitch_auth():
        data = request.get_json()
        code = data.get("code")

        if not code:
            return jsonify({"error": "Missing authorization code"}), 400

        try:
            login_response = login_account(
                auth_code=code,
                auth_provider=auth_provider,
                user_account_repo=account_repository,
            )
        except AuthException as e:
            return jsonify({"error": str(e)}), 400

        return jsonify(login_response._asdict())

    return bp
