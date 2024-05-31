from flask import Blueprint, jsonify, request

from src.application.interfaces.repositories.account import IAccountRepository
from src.application.use_cases.auth import login_account
from src.infrastructure.services.auth import AuthException, IAuthProvider


def create_auth_blueprint(
    auth_provider: IAuthProvider, account_repository: IAccountRepository
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
