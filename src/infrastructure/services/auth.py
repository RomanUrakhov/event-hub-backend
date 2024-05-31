from abc import ABC, abstractmethod
from typing import NamedTuple

import jwt
import requests
from jwt import InvalidTokenError
from jwt.api_jwt import decode

import src.config as config


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
    def validate_token(self, token: str) -> bool:
        pass


class TwitchAuthProvider(IAuthProvider):
    AUTH_SERVER = "id.twitch.tv/oauth2"
    TOKEN_ENDPOINT = f"https://{AUTH_SERVER}/token"

    def authenticate_user(self, code: str) -> AuthPayload:
        payload = {
            "client_id": config.TWITCH_CLIENT_ID,
            "client_secret": config.TWITCH_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": config.TWITCH_REDIRECT_URI,
        }

        try:
            response = requests.post(TwitchAuthProvider.TOKEN_ENDPOINT, data=payload)
            response.raise_for_status()
            auth_data = response.json()

            id_token = auth_data.get("id_token")

            decoded_token = jwt.decode(id_token, options={"verify_signature": False})
            user_avatar = decoded_token.get("picture")
            user_username = decoded_token.get("preferred_username")

            return AuthPayload(
                access_token=auth_data["id_token"],
                refresh_token=auth_data["refresh_token"],
                user_payload=UserPayload(
                    external_id=decoded_token["sub"],
                    avatar=user_avatar,
                    name=user_username,
                ),
            )
        except Exception:
            raise TwitchAuthException("Failed to authenticate user")

    def validate_token(self, token: str) -> UserPayload:
        oidc_config = requests.get(
            self.OPENID_CONFIG_URL_TEMPLATE.format(server=self.AUTH_SERVER)
        ).json()

        signing_algos = oidc_config["id_token_signing_alg_values_supported"]
        jwks_client = jwt.PyJWKClient(oidc_config["jwks_uri"])

        try:
            signing_key = jwks_client.get_signing_key_from_jwt(token)

            auth_payload = decode(
                token,
                key=signing_key.key,
                algorithms=signing_algos,
                audience=config.TWITCH_CLIENT_ID,
            )
        except InvalidTokenError as e:
            raise AuthException("Invalid token") from e

        return UserPayload(
            external_id=auth_payload["sub"],
            avatar=auth_payload["picture"],
            name=auth_payload["preferred_username"],
        )
