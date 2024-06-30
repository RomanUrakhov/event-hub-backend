from flask import Flask

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from infrastructure.dao.event import MySQLEventDAO
from infrastructure.dao.streamer import MySQLStreamerDAO
from infrastructure.repositories.participation import (
    MySQLParticipationRepository,
)
from infrastructure.repositories.streamer import (
    MySQLStreamerRepository,
)
from config import Config
from infrastructure.repositories.event import (
    MySQLEventRepository,
)


def create_app() -> Flask:
    app = Flask(__name__)

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


def _register_blueprints(app: Flask, session_factory):
    from .controllers.event import create_event_blueprint
    from .controllers.misc import create_misc_blueprint
    from .controllers.streamer import create_streamer_blueprint

    # TODO: maybe create a session per request - not on app startup
    session = session_factory()

    event_repo = MySQLEventRepository(session)
    streamer_repo = MySQLStreamerRepository(session)
    participation_repo = MySQLParticipationRepository(session)

    event_dao = MySQLEventDAO(session)
    streamer_dao = MySQLStreamerDAO(session)

    # TODO: find the way to setup global API prefix at once and not duplicate for every blueprint
    event_bp = create_event_blueprint(
        event_repo=event_repo,
        streamer_repo=streamer_repo,
        participation_repo=participation_repo,
        event_dao=event_dao,
    )
    app.register_blueprint(event_bp, url_prefix=app.config["APPLICATION_ROOT"])

    misc_bp = create_misc_blueprint()
    app.register_blueprint(misc_bp, url_prefix=app.config["APPLICATION_ROOT"])

    streamer_bp = create_streamer_blueprint(
        streamer_repository=streamer_repo,
        streamer_dao=streamer_dao,
    )
    app.register_blueprint(streamer_bp, url_prefix=app.config["APPLICATION_ROOT"])

    return app
