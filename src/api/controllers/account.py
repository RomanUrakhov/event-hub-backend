from flask import g
from apiflask import APIBlueprint
from api.schemas.account import (
    AccountAccessQueryParams,
    AccountAccessSchema,
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
    bp = APIBlueprint("account", __name__)

    def _get_event_access(access):
        return {
            "can_enroll_streamers": access.can_enroll_streamers_on_event()
            if access
            else False,
            "can_moderate_highlights": access.can_moderate_highlights_on_event()
            if access
            else False,
        }

    @bp.route("/account/access", methods=["GET"])
    @bp.input(AccountAccessQueryParams, location="query")
    @bp.output(AccountAccessSchema)
    @token_required(auth_provider=auth_provider, account_repository=account_repo)
    def get_account_access(query_data):
        user_account = g.user_account
        event_id = query_data.get("event_id")

        global_access = account_app_access_repo.account_has_global_access(
            user_account.id
        )

        if event_id:
            access = account_event_access_repo.get_account_access(
                user_account.id, event_id
            )
            events = {event_id: _get_event_access(access)}
        else:
            events = {
                access.event_id: _get_event_access
                for access in account_event_access_repo.list_account_accesses(
                    user_account.id
                )
            }

        return {
            "global_access": global_access,
            "events": events,
        }

    return bp
