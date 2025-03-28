from apiflask import APIFlask

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from api.controllers.auth import create_auth_blueprint
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
from config import Config
from infrastructure.repositories.event import (
    MySQLEventRepository,
)


def create_app() -> APIFlask:
    app = APIFlask(__name__, docs_ui="redoc")
    app.security_schemes = app.security_schemes = {
        "TwitchJWTAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token from Twitch, passed in the Authorization header as 'Bearer <token>'.",
        }
    }
    app.config["SERVERS"] = [
        # TODO: should this 'localhost' hardcodes be configurated? I think so...
        {"name": "Dev Server", "url": "http://localhost:5000"},
        # TODO: add production-ready server when it's ready :)
    ]

    config = Config()
    app.config.from_object(config)

    engine = create_engine(
        URL.create(
            drivername=config.DB_DRIVER,
            username=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=int(config.DB_PORT),
            database=config.DB_NAME,
        )
    )
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    _register_blueprints(app, session_factory)

    return app


def _register_blueprints(app: APIFlask, session_factory):
    from .controllers.event import create_event_blueprint
    from .controllers.misc import create_misc_blueprint
    from .controllers.streamer import create_streamer_blueprint
    from .controllers.account import create_account_blueprint

    # TODO: maybe create a session per request - not on app startup
    session = session_factory()

    event_repo = MySQLEventRepository(session)
    streamer_repo = MySQLStreamerRepository(session)
    participation_repo = MySQLParticipationRepository(session)
    account_repository = MySQLUserAccountRepository(session)
    account_event_access_repository = MySQLAccountEventAccessRepository(session)
    account_app_access_repo = MySQLAccountAppAccessRepository(session)

    event_dao = MySQLEventDAO(session)
    streamer_dao = MySQLStreamerDAO(session)

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
