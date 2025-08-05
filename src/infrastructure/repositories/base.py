from flask_sqlalchemy import SQLAlchemy


class BaseSQLAlchemyRepository:
    def __init__(self, db: SQLAlchemy):
        self._db = db
        self._session = db.session
