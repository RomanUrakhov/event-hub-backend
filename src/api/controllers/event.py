from flask import g, url_for
from apiflask import APIBlueprint, abort

from api.controllers.auth import token_required
from application.interfaces.dao.event import IEventDAO
from application.interfaces.repositories.account import (
    IAccountAppAccessRepository,
    IAccountEventAccessRepository,
    IUserAccountRepository,
)
from application.interfaces.repositories.participation import IParticipationRepository
from application.interfaces.repositories.streamer import IStreamerRepository
from application.interfaces.services.auth import IAuthProvider
from application.use_cases.dto.event import (
    AttachHighlightsCommand,
    CreateEventCommand,
    EntrollStreamerOnEventCommand,
)
from domain.exceptions.account import (
    AccountDoesNotHaveAccessException,
    AccountDoesNotHaveCreatorAccessException,
)
from domain.exceptions.event import EventAlreadyExistsException, EventNotFoundException
from domain.models.account import UserAccount
from src.api.schemas.event import (
    AttachHighlightsRequestSchema,
    AttachHighlightsResponseSchema,
    CreateEventRequestSchema,
    CreateEventResponseSchema,
    EnrollStreamerRequestSchema,
    GetEventByIdResponseSchema,
    ListAllEventsResponseSchema,
)
from src.application.interfaces.repositories.event import IEventRepository
from src.application.use_cases.event import (
    AttachHightlihtsToEvent,
    EntrollStreamersOnEvent,
    GetEventById,
    CreateEvent,
    ListAllEvents,
)

# TODO: make custom error schemas for my domain exception in order not to repeat myself in @bp.doc()


def create_event_blueprint(
    auth_provider: IAuthProvider,
    event_repo: IEventRepository,
    event_dao: IEventDAO,
    streamer_repo: IStreamerRepository,
    participation_repo: IParticipationRepository,
    account_repo: IUserAccountRepository,
    account_event_access_repo: IAccountEventAccessRepository,
    account_app_access_repo: IAccountAppAccessRepository,
):
    bp = APIBlueprint("event", __name__)

    @bp.route("/events/<string:id>", methods=["GET"])
    @bp.output(GetEventByIdResponseSchema)
    @bp.doc(
        responses={
            404: {
                "description": "Event not found",
                "content": {
                    "application/json": {
                        "example": {
                            "status_code": 404,
                            "message": "Event not found",
                            "extra_data": {"event_id": "123"},
                        }
                    }
                },
            }
        }
    )
    def get_event(id: str):
        use_case = GetEventById(event_dao)
        try:
            event_dto = use_case(id)
        except EventNotFoundException as e:
            abort(404, message="Event not found", extra_data={"event_id": e.event_id})
        return GetEventByIdResponseSchema.from_dto(event_dto)

    @bp.route("/events/", methods=["GET"])
    @bp.output(ListAllEventsResponseSchema)
    def list_events():
        # TODO: add pagination
        use_case = ListAllEvents(event_dao)
        events_dtos = use_case()
        return ListAllEventsResponseSchema.from_dto(events_dtos)

    @bp.route("/events", methods=["POST"])
    @bp.input(CreateEventRequestSchema)
    @bp.output(CreateEventResponseSchema, status_code=201)
    @bp.doc(
        security=[{"TwitchJWTAuth": []}],
        responses={
            403: {
                "description": "Forbidden - No creator access",
                "content": {
                    "application/json": {
                        "example": {
                            "status_code": 403,
                            "message": "User does not have creator access",
                            "extra_data": {"account_id": "string <uuid>"},
                        }
                    }
                },
            },
            409: {
                "description": "Conflict - Event already exists",
                "content": {
                    "application/json": {
                        "example": {
                            "status_code": 409,
                            "message": "Event with such name already exists",
                            "extra_data": {"event_name": "MyEvent"},
                        }
                    }
                },
            },
        },
    )
    @token_required(auth_provider=auth_provider, account_repository=account_repo)
    def create_event(json_data):
        user_account: UserAccount = g.user_account
        json_data["author_id"] = user_account.id
        command = CreateEventCommand.model_validate(json_data)
        use_case = CreateEvent(
            event_repo, streamer_repo, participation_repo, account_app_access_repo
        )
        try:
            event_id = use_case(command)
        except AccountDoesNotHaveCreatorAccessException as e:
            abort(403, message=str(e), extra_data={"account_id": e.account_id})
        except EventAlreadyExistsException as e:
            abort(
                409,
                message="Event with such name already exists",
                extra_data={"event_name": e.event_name},
            )
        return {
            "id": event_id,
            "url": url_for("event.get_event", id=event_id, _external=True),
        }

    @bp.route("/events/<string:event_id>/streamers", methods=["POST"])
    @bp.input(EnrollStreamerRequestSchema)
    @bp.doc(
        security=[{"TwitchJWTAuth": []}],
        responses={
            403: {
                "description": "Forbidden - User lacks access",
                "content": {
                    "application/json": {
                        "example": {
                            "status_code": 403,
                            "message": "User does not have access to this event",
                            "extra_data": {"account_id": "456"},
                        }
                    }
                },
            },
            404: {
                "description": "Not Found - Event does not exist",
                "content": {
                    "application/json": {
                        "example": {
                            "status_code": 404,
                            "message": "Event not found",
                            "extra_data": {"event_id": "123"},
                        }
                    }
                },
            },
        },
    )
    @token_required(auth_provider=auth_provider, account_repository=account_repo)
    def entroll_streamer_on_event(event_id: str, json_data):
        user_account: UserAccount = g.user_account
        json_data["event_id"] = event_id
        json_data["author_id"] = user_account.id
        command = EntrollStreamerOnEventCommand.model_validate(json_data)
        use_case = EntrollStreamersOnEvent(
            event_repo=event_repo,
            streamer_repository=streamer_repo,
            participation_repository=participation_repo,
            account_event_access_repository=account_event_access_repo,
        )
        try:
            use_case(command)
        except AccountDoesNotHaveAccessException as e:
            abort(403, message=str(e), extra_data={"account_id": e.account_id})
        except EventNotFoundException as e:
            abort(404, message="Event not found", extra_data={"event_id": e.event_id})
        return {"message": "Streamer enrolled successfully"}, 200

    @bp.route("/events/<string:event_id>/hightlights", methods=["POST"])
    @bp.input(AttachHighlightsRequestSchema)
    @bp.output(AttachHighlightsResponseSchema, status_code=201)
    @bp.doc(
        security=[{"TwitchJWTAuth": []}],
        responses={
            403: {
                "description": "Forbidden - User lacks access",
                "content": {
                    "application/json": {
                        "example": {
                            "status_code": 403,
                            "message": "User does not have access to this event",
                            "extra_data": {"account_id": "456"},
                        }
                    }
                },
            },
            404: {
                "description": "Not Found - Event does not exist",
                "content": {
                    "application/json": {
                        "example": {
                            "status_code": 404,
                            "message": "Event not found",
                            "extra_data": {"event_id": "123"},
                        }
                    }
                },
            },
        },
    )
    @token_required(auth_provider=auth_provider, account_repository=account_repo)
    def attach_highlights(event_id: str, json_data):
        user_account: UserAccount = g.user_account
        json_data["event_id"] = event_id
        json_data["author_id"] = user_account.id
        command = AttachHighlightsCommand.model_validate(json_data)
        use_case = AttachHightlihtsToEvent(event_repo, account_event_access_repo)
        try:
            attached_urls = use_case(command)
        except AccountDoesNotHaveAccessException as e:
            abort(403, message=str(e), extra_data={"account_id": e.account_id})
        except EventNotFoundException as e:
            abort(404, message="Event not found", extra_data={"event_id": e.event_id})
        return {"event_id": event_id, "highlights": attached_urls}

    return bp
