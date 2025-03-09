from abc import ABC, abstractmethod
from typing import NamedTuple

import jwt
import requests
from jwt import InvalidTokenError
from jwt.api_jwt import decode


class AuthException(Exception):
    pass


class TwitchAuthException(AuthException):
    pass


class UserPayload(NamedTuple):
    external_id: str
    avatar: str
    name: str


class AuthPayload(NamedTuple):
    access_token: str
    refresh_token: str
    user_payload: UserPayload

    def to_dict(self):
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "user_payload": {
                "external_id": self.user_payload.external_id,
                "user_avatar": self.user_payload.avatar,
                "user_name": self.user_payload.name,
            },
        }


class IAuthProvider(ABC):
    OPENID_CONFIG_URL_TEMPLATE = "https://{server}/.well-known/openid-configuration"

    @abstractmethod
    def authenticate_user(self, code: str) -> AuthPayload:
        pass

    @abstractmethod
    def validate_token(self, token: str) -> UserPayload:
        pass

    @abstractmethod
    def refresh_token(self, refresh_token: str) -> AuthPayload:
        pass
