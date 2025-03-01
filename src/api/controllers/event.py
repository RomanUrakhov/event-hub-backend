from flask import Blueprint, jsonify, request, url_for, g
from pydantic import ValidationError

from api.controllers.auth import token_required
from application.interfaces.dao.event import IEventDAO
from application.interfaces.repositories.account import (
    IAccountEventAccessRepository,
    IUserAccountRepository,
)
from application.interfaces.repositories.participation import IParticipationRepository
from application.interfaces.repositories.streamer import IStreamerRepository
from application.interfaces.services.auth import IAuthProvider
from application.use_cases.dto.event import AttachHighlightsCommand, CreateEventCommand
from domain.exceptions.account import AccountDoesNotHaveAccessException
from domain.exceptions.event import EventAlreadyExistsException, EventNotFoundException
from domain.models.account import UserAccount
from src.api.schemas.event import GetEventByIdResponse, ListAllEventsResponse
from src.application.interfaces.repositories.event import IEventRepository
from src.application.use_cases.event import (
    AttachHightlihtsToEvent,
    GetEventById,
    CreateEvent,
    ListAllEvents,
)


def create_event_blueprint(
    auth_provider: IAuthProvider,
    event_repo: IEventRepository,
    event_dao: IEventDAO,
    streamer_repo: IStreamerRepository,
    participation_repo: IParticipationRepository,
    account_repo: IUserAccountRepository,
    account_event_access_repo: IAccountEventAccessRepository,
):
    bp = Blueprint("event", __name__)

    @bp.route("/events/<string:id>", methods=["GET"])
    def get_event(id: str):
        use_case = GetEventById(event_dao)
        event_dto = use_case(id)
        event_reponse = GetEventByIdResponse.from_dto(event_dto)
        return jsonify(event_reponse.model_dump()), 200

    @bp.route("/events/", methods=["GET"])
    def list_events():
        # TODO: add pagination
        use_case = ListAllEvents(event_dao)
        events_dtos = use_case()
        events_response = ListAllEventsResponse.from_dto(events_dtos)
        return jsonify(events_response.model_dump()), 200

    @bp.route("/events", methods=["POST"])
    def create_event():
        command = CreateEventCommand.model_validate(request.json)
        use_case = CreateEvent(event_repo, streamer_repo, participation_repo)
        event_id = use_case(command)
        return jsonify(
            {
                "url": url_for("event.get_event", id=event_id, _external=True),
                "id": event_id,
            }
        ), 201

    @bp.route("/events/<string:event_id>/hightlights", methods=["POST"])
    @token_required(auth_provider=auth_provider, account_repository=account_repo)
    def attach_highlights(event_id: str):
        user_account: UserAccount = g.user_account
        payload = request.get_json()
        payload["event_id"] = event_id
        payload["author_id"] = user_account.id
        command = AttachHighlightsCommand.model_validate(payload)
        use_case = AttachHightlihtsToEvent(event_repo, account_event_access_repo)
        attached_urls = use_case(command)
        return jsonify({"event_id": event_id, "highlights": attached_urls}), 201

    @bp.errorhandler(EventNotFoundException)
    def handle_event_not_found_exception(e: EventNotFoundException):
        return jsonify({"error": "Event not found", "event_id": e.event_id}), 404

    @bp.errorhandler(ValidationError)
    def handle_validation_error(e: ValidationError):
        return jsonify(e.errors()), 400

    @bp.errorhandler(EventAlreadyExistsException)
    def handle_event_already_exists_exception(e: EventAlreadyExistsException):
        return jsonify(
            {"error": "Event with such name already exists", "event_name": e.event_name}
        ), 409

    @bp.errorhandler(AccountDoesNotHaveAccessException)
    def handle_account_does_not_have_access_exception(
        e: AccountDoesNotHaveAccessException,
    ):
        return jsonify(
            {"error": str(e), "account_id": e.account_id, "event_id": e.event_id}
        ), 403

    return bp
