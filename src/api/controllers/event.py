from flask import Blueprint, jsonify

from src.api.schemas.event import GetEventByIdResponse
from src.application.interfaces.repositories.event import IEventRepository
from src.application.use_cases.event import GetEventById
from src.application.use_cases.exceptions.event import EventNotFoundException


def create_event_blueprint(event_repo: IEventRepository):
    bp = Blueprint("event", __name__)

    @bp.route("/events/<string:id>", methods=["GET"])
    def get_event(id: str):
        use_case = GetEventById(event_repo)
        event_dto = use_case(id)
        event_reponse = GetEventByIdResponse.from_dto(event_dto)
        return jsonify(event_reponse.model_dump()), 200

    @bp.errorhandler(EventNotFoundException)
    def handle_event_not_found_exception(e: EventNotFoundException):
        return jsonify({"error": "Event not found", "event_id": e.event_id})

    return bp
