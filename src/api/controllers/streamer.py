from apiflask import APIBlueprint, abort
from api.schemas.streamer import (
    CreateStreamerRequest,
    CreateStreamerResponse,
    GetStreamerDetailsResponse,
    StreamerExistsErrorSchema,
)
from application.interfaces.dao.streamer import IStreamerDAO
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
    auth_required,
):
    bp = APIBlueprint("streamer", __name__)

    @bp.route("/streamers", methods=["POST"])
    @bp.doc(
        operation_id="createStreamer",
        security=[{"InternalBearerAuth": []}],
        responses={
            409: {
                "description": "Conflict error",
                "content": {
                    "application/json": {
                        "schema": {"oneOf": [StreamerExistsErrorSchema]}
                    }
                },
            }
        },
    )
    @bp.input(CreateStreamerRequest)
    @bp.output(CreateStreamerResponse, status_code=201)
    @auth_required
    def create_streamer(json_data):
        command = CreateStreamerCommand.model_validate(json_data)
        use_case = CreateStreamer(streamer_repository)
        try:
            streamer_id = use_case(command)
        except StreamerAlreadyExistsException as e:
            abort(
                409,
                str(e),
                detail={
                    "code": "STREAMER_EXISTS",
                    "streamer_id": e.streamer_id,
                    "twitch_id": e.twitch_id,
                },
            )
        return CreateStreamerResponse.from_dto(streamer_id=streamer_id)

    @bp.route("/streamers/<string:streamer_id>", methods=["GET"])
    @bp.doc(operation_id="getStreamerById")
    @bp.output(GetStreamerDetailsResponse)
    def get_streamer(streamer_id: str):
        use_case = GetStreamerDetails(streamer_dao)
        try:
            streamer = use_case(streamer_id=streamer_id)
        except StreamerNotExistsException as e:
            abort(404, str(e))
        return GetStreamerDetailsResponse.from_dto(streamer)

    return bp
