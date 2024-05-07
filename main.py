import io
from functools import wraps

from flask import Flask, request, jsonify, g, send_file

from src.api.schemas.event import EventCreateRequest, EventUpdateRequest
from src.domain.user_account import SpecificEventAction

from src.repository.event import FakeEventRepository
from src.repository.user_account import FakeUserAccountRepository
from src.services.auth import TwitchAuthProvider, AuthException
from src.services.file_manager import FakeFileManager
from src.usecases.account_cases import login_account, has_event_access, has_system_access
from src.usecases import event_cases, image_cases

app = Flask(__name__)


def require_authentication(func):
    auth_service = TwitchAuthProvider()

    @wraps(func)
    def wrapper(*args, **kwargs):
        id_token = request.cookies.get('id_token')

        if not id_token:
            return jsonify({'error': 'Unauthorized'}), 401

        try:
            user_payload = auth_service.validate_token(id_token)
        except AuthException:
            return jsonify({'error': 'Unauthorized'}), 401

        g.external_user_id = user_payload.external_id

        return func(*args, **kwargs)

    return wrapper


def require_access(event_id_field: str = None, event_action: SpecificEventAction = None):
    def decorator(func):

        user_repository = FakeUserAccountRepository()

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                user_id = g.external_user_id
            except AttributeError as e:
                raise AttributeError(
                    f'@{require_access.__name__} requires '
                    f'@{require_authentication.__name__} decorator first'
                ) from e

            event_id = None
            if event_id_field:
                event_id = kwargs[event_id_field]

            if event_id:
                has_access = has_event_access(
                    user_id=user_id,
                    event_id=event_id,
                    action=event_action,
                    user_account_repository=user_repository
                )
            else:
                has_access = has_system_access(
                    user_id=user_id,
                    user_account_repository=user_repository
                )

            if not has_access:
                return jsonify({'error': 'Access denied'}), 403

            return func(*args, **kwargs)

        return wrapper

    return decorator


@app.route('/api/auth/twitch', methods=['POST'])
def twitch_auth():
    data = request.get_json()
    code = data.get('code')

    if not code:
        return jsonify({'error': 'Missing authorization code'}), 400

    auth_provider = TwitchAuthProvider()
    account_repo = FakeUserAccountRepository()

    try:
        login_response = login_account(
            auth_code=code,
            auth_provider=auth_provider,
            user_account_repo=account_repo
        )
    except AuthException as e:
        return jsonify({'error': str(e)}), 400

    return jsonify(login_response._asdict())


@app.route('/api/events', methods=['POST'])
# @require_authentication
# @require_access()
def create_event():
    data = request.get_json()
    event_data = EventCreateRequest(**data)

    event_repo = FakeEventRepository(events=[])

    create_event_response = event_cases.create_event(
        event_data=event_data,
        event_repo=event_repo
    )
    return jsonify(create_event_response.model_dump()), 201


@app.route('/api/events/<event_id>', methods=['PUT'])
@require_authentication
@require_access(
    event_id_field='event_id',
    event_action=SpecificEventAction.UPDATE_METADATA
)
def update_event(event_id: str):
    data = request.get_json()
    event_data = EventUpdateRequest(id_=event_id, **data)

    event_repo = FakeEventRepository(events=[])
    event_cases.update_event(
        event_data=event_data,
        event_repo=event_repo
    )


@app.route('/api/images', methods=['POST'])
@require_authentication
def upload_image():
    if not request.files:
        return jsonify({'error': 'Missing file'}), 400
    if 'image' not in request.files:
        return jsonify({'error': 'Missing image file'}), 400

    image = request.files['image']

    file_manager = FakeFileManager()

    file_id = image_cases.upload_image(
        file=image.stream.read(),
        file_manager=file_manager,
    )

    return jsonify({
        'id': file_id,
        'url': f'/api/images/{file_id}'
    }), 201


@app.route('/api/images/<image_id>', methods=['GET'])
@require_authentication
def get_image(image_id: str):
    file_manager = FakeFileManager()

    file = image_cases.get_image(
        file_id=image_id,
        file_manager=file_manager,
    )

    return send_file(
        io.BytesIO(file),
        mimetype='image/png'
    )
