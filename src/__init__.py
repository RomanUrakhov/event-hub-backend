from apiflask import APIFlask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from api.controllers.account import create_account_blueprint
from api.controllers.auth import create_auth_blueprint
from api.controllers.event import create_event_blueprint
from api.controllers.misc import create_misc_blueprint
from api.controllers.streamer import create_streamer_blueprint

from infrastructure.dao.event import MySQLEventDAO
from infrastructure.dao.streamer import MySQLStreamerDAO
from infrastructure.repositories.participation import (
    MySQLParticipationRepository,
)
from infrastructure.repositories.user_account import (
    MySQLAccountAppAccessRepository,
    MySQLAccountEventAccessRepository,
    MySQLUserAccountRepository,
)
from infrastructure.services.auth import TwitchAuthProvider
from infrastructure.repositories.streamer import (
    MySQLStreamerRepository,
)
from infrastructure.repositories.event import (
    MySQLEventRepository,
)

from domain import db

from config import Config
from infrastructure.services.twitch_service import TwitchService


def create_app() -> APIFlask:
    app = APIFlask(__name__, docs_ui="redoc")

    config = Config()
    app.config.from_object(config)

    CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)

    app.security_schemes = app.security_schemes = {
        "TwitchJWTAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token from Twitch, passed in the Authorization header as 'Bearer <token>'.",
        }
    }

    _register_blueprints(app, db)

    return app


def _register_blueprints(app: APIFlask, db: SQLAlchemy):
    event_repo = MySQLEventRepository(db)
    streamer_repo = MySQLStreamerRepository(db)
    participation_repo = MySQLParticipationRepository(db)
    account_repository = MySQLUserAccountRepository(db)
    account_event_access_repository = MySQLAccountEventAccessRepository(db)
    account_app_access_repo = MySQLAccountAppAccessRepository(db)

    event_dao = MySQLEventDAO(db)
    streamer_dao = MySQLStreamerDAO(db)

    twitch_service = TwitchService(
        app.config["TWITCH_CLIENT_ID"], client_secret=app.config["TWITCH_CLIENT_SECRET"]
    )

    auth_provider = TwitchAuthProvider(
        app.config["TWITCH_CLIENT_ID"],
        app.config["TWITCH_CLIENT_SECRET"],
        app.config["TWITCH_REDIRECT_URI"],
    )

    # TODO: find the way to setup global API prefix at once and not duplicate for every blueprint
    auth_bp = create_auth_blueprint(
        auth_provider=auth_provider, account_repository=account_repository
    )
    app.register_blueprint(auth_bp, url_prefix=app.config["APPLICATION_ROOT"])

    event_bp = create_event_blueprint(
        auth_provider=auth_provider,
        event_repo=event_repo,
        streamer_repo=streamer_repo,
        participation_repo=participation_repo,
        event_dao=event_dao,
        twitch_service=twitch_service,
        account_repo=account_repository,
        account_event_access_repo=account_event_access_repository,
        account_app_access_repo=account_app_access_repo,
    )
    app.register_blueprint(event_bp, url_prefix=app.config["APPLICATION_ROOT"])

    misc_bp = create_misc_blueprint(
        auth_provider=auth_provider, account_repository=account_repository
    )
    app.register_blueprint(misc_bp, url_prefix=app.config["APPLICATION_ROOT"])

    streamer_bp = create_streamer_blueprint(
        streamer_repository=streamer_repo,
        streamer_dao=streamer_dao,
        auth_provider=auth_provider,
        account_repo=account_repository,
    )
    app.register_blueprint(streamer_bp, url_prefix=app.config["APPLICATION_ROOT"])

    account_bp = create_account_blueprint(
        account_repo=account_repository,
        account_event_access_repo=account_event_access_repository,
        account_app_access_repo=account_app_access_repo,
        auth_provider=auth_provider,
    )
    app.register_blueprint(account_bp, url_prefix=app.config["APPLICATION_ROOT"])

    return app
