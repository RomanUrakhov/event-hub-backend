from flask import Blueprint, jsonify, request
from api.schemas.streamer import CreateStreamerResponse
from application.use_cases.dto.streamer import CreateStreamerCommand
from application.interfaces.repositories.streamer import IStreamerRepository
from application.use_cases.streamer import CreateStreamer


def create_streamer_blueprint(streamer_repository: IStreamerRepository):
    bp = Blueprint("streamer", __name__)

    @bp.route("/streamers", methods=["POST"])
    def create_streamer():
        command = CreateStreamerCommand.model_validate(request.json)
        use_case = CreateStreamer(streamer_repository)
        streamer_id = use_case(command)
        response = CreateStreamerResponse(id=streamer_id)
        return jsonify(response.model_dump()), 201

    @bp.route("/streamers/<string:streamer_id>", methods=["GET"])
    def get_streamer(streamer_id: str):
        return jsonify(
            {
                "id": "123",
            }
        ), 200

    return bp
