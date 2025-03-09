from flask import Blueprint, jsonify, request, g
from api.schemas.account import (
    AccountAccessSchema,
    EventAccessSchema,
    EventSpecificAccessSchema,
)
from application.interfaces.services.auth import IAuthProvider
from application.interfaces.repositories.account import (
    IAccountAppAccessRepository,
    IAccountEventAccessRepository,
    IUserAccountRepository,
)
from api.controllers.auth import token_required


def create_account_blueprint(
    account_repo: IUserAccountRepository,
    account_event_access_repo: IAccountEventAccessRepository,
    account_app_access_repo: IAccountAppAccessRepository,
    auth_provider: IAuthProvider,
):
    bp = Blueprint("account", __name__)

    @bp.route("/account/access", methods=["GET"])
    @token_required(auth_provider=auth_provider, account_repository=account_repo)
    def get_account_access():
        user_account = g.user_account
        event_id = request.args.get("event_id")

        if event_id:
            access = account_event_access_repo.get_account_access(
                user_account.id, event_id
            )
            result = EventSpecificAccessSchema(
                event_id=event_id,
                can_enroll_streamers=access.can_enroll_streamers_on_event()
                if access
                else False,
                can_moderate_highlights=access.can_moderate_highlights_on_event()
                if access
                else False,
            )
            return jsonify(result.model_dump())

        global_access = account_app_access_repo.account_has_global_access(
            user_account.id
        )

        event_access = {}
        for access in account_event_access_repo.list_account_accesses(user_account.id):
            event_access[access.event_id] = EventAccessSchema(
                can_enroll_streamers=access.can_enroll_streamers_on_event(),
                can_moderate_highlights=access.can_moderate_highlights_on_event(),
            )

        result = AccountAccessSchema(global_access=global_access, events=event_access)

        return jsonify(result.model_dump())

    return bp
