from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from api.controllers.auth import token_required
from api.schemas.streamer import CreateStreamerResponse, GetStreamerDetailsResponse
from application.interfaces.dao.streamer import IStreamerDAO
from application.interfaces.services.auth import IAuthProvider
from application.use_cases.dto.streamer import CreateStreamerCommand
from application.interfaces.repositories.streamer import IStreamerRepository
from application.use_cases.streamer import CreateStreamer, GetStreamerDetails
from domain.exceptions.streamer import (
    StreamerAlreadyExistsException,
    StreamerNotExistsException,
)


def create_streamer_blueprint(
    streamer_repository: IStreamerRepository,
    streamer_dao: IStreamerDAO,
    auth_provider: IAuthProvider,
):
    bp = Blueprint("streamer", __name__)

    @bp.route("/streamers", methods=["POST"])
    @token_required(auth_provider)
    def create_streamer():
        command = CreateStreamerCommand.model_validate(request.json)
        use_case = CreateStreamer(streamer_repository)
        streamer_id = use_case(command)
        response = CreateStreamerResponse(id=streamer_id)
        return jsonify(response.model_dump()), 201

    @bp.route("/streamers/<string:streamer_id>", methods=["GET"])
    def get_streamer(streamer_id: str):
        use_case = GetStreamerDetails(streamer_dao)
        streamer = use_case(streamer_id=streamer_id)
        response = GetStreamerDetailsResponse.from_dto(streamer)
        return jsonify(response.model_dump()), 200

    @bp.errorhandler(StreamerNotExistsException)
    def handle_streamer_not_found_exception(e: StreamerNotExistsException):
        return jsonify(
            {"error": "Streamer not found", "streamer_id": e.streamer_id}
        ), 404

    @bp.errorhandler(StreamerAlreadyExistsException)
    def handle_streamer_already_exists_exception(e: StreamerAlreadyExistsException):
        return jsonify(
            {
                "error": "Streamer with such twitch ID already exists",
                "streamer_id": e.streamer_id,
                "twitch_id": e.twitch_id,
            }
        ), 409

    @bp.errorhandler(ValidationError)
    def handle_validation_error(e: ValidationError):
        return jsonify(e.errors()), 400

    return bp
