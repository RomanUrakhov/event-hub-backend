from flask import Blueprint, jsonify, request, url_for
from pydantic import ValidationError

from application.use_cases.dto.event import CreateEventCommand
from src.api.schemas.event import GetEventByIdResponse
from src.application.interfaces.repositories.event import IEventRepository
from src.application.use_cases.event import GetEventById, CreateEvent
from src.application.use_cases.exceptions.event import (
    EventAlreadyExistsException,
    EventNotFoundException,
)


def create_event_blueprint(event_repo: IEventRepository):
    bp = Blueprint("event", __name__)

    @bp.route("/events/<string:id>", methods=["GET"])
    def get_event(id: str):
        use_case = GetEventById(event_repo)
        event_dto = use_case(id)
        event_reponse = GetEventByIdResponse.from_dto(event_dto)
        return jsonify(event_reponse.model_dump()), 200

    @bp.route("/events", methods=["POST"])
    def create_event():
        command = CreateEventCommand.model_validate(request.json)
        use_case = CreateEvent(event_repo)
        event_id = use_case(command)
        return jsonify(
            {
                "url": url_for("event.get_event", id=event_id, _external=True),
                "id": event_id,
            }
        ), 201

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

    return bp
