from apiflask import APIBlueprint, abort
from api.controllers.auth import token_required
from api.schemas.streamer import (
    CreateStreamerRequest,
    CreateStreamerResponse,
    GetStreamerDetailsResponse,
)
from application.interfaces.dao.streamer import IStreamerDAO
from application.interfaces.repositories.account import IUserAccountRepository
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
    account_repo: IUserAccountRepository,
):
    bp = APIBlueprint("streamer", __name__)

    @bp.route("/streamers", methods=["POST"])
    @bp.doc(security=[{"TwitchJWTAuth": []}])
    @bp.input(CreateStreamerRequest)
    @bp.output(CreateStreamerResponse, status_code=201)
    @token_required(auth_provider=auth_provider, account_repository=account_repo)
    def create_streamer(json_data):
        command = CreateStreamerCommand.model_validate(json_data)
        use_case = CreateStreamer(streamer_repository)
        try:
            streamer_id = use_case(command)
        except StreamerAlreadyExistsException as e:
            abort(
                409,
                str(e),
                detail={"streamer_id": e.streamer_id, "twitch_id": e.twitch_id},
            )
        return CreateStreamerResponse.from_dto(streamer_id=streamer_id)

    @bp.route("/streamers/<string:streamer_id>", methods=["GET"])
    @bp.output(GetStreamerDetailsResponse)
    def get_streamer(streamer_id: str):
        use_case = GetStreamerDetails(streamer_dao)
        try:
            streamer = use_case(streamer_id=streamer_id)
        except StreamerNotExistsException as e:
            abort(404, str(e))
        return GetStreamerDetailsResponse.from_dto(streamer)

    return bp
