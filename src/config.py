import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # --- Application Settings ---
    APPLICATION_HOST = os.getenv("APPLICATION_HOST", "0.0.0.0")
    APPLICATION_PORT = int(os.getenv("APPLICATION_PORT", 5000))
    APPLICATION_ROOT = "/api"
    # TODO: deal with processing static files
    APPLICATION_STATIC_DIR = "static/images"
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]

    # --- Database Settings ---
    DB_DRIVER = os.getenv("DB_DRIVER", "")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "")
    DB_NAME = os.getenv("DB_NAME")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # --- External Services ---
    TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
    TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
    TWITCH_REDIRECT_URI = os.getenv("TWITCH_REDIRECT_URI")
