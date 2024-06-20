from flask import Blueprint, jsonify, request, url_for
from api.schemas.streamer import CreateStreamerCommand
from application.interfaces.repositories.streamer import IStreamerRepository
from application.use_cases.streamer import CreateStreamer


def create_streamer_blueprint(streamer_repository: IStreamerRepository):
    bp = Blueprint("streamer", __name__)

    @bp.route("/streamer", methods=["POST"])
    def create_streamer():
        command = CreateStreamerCommand.model_validate(request.json)
        use_case = CreateStreamer(streamer_repository)
        streamer_id = use_case(command)
        return jsonify(
            {
                "url": url_for("streamer.get_streamer", id=streamer_id, _external=True),
                "id": streamer_id,
            }
        ), 201
