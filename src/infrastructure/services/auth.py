import jwt
import requests
from jwt import InvalidTokenError
from jwt.api_jwt import decode

from application.interfaces.services.auth import (
    AuthException,
    AuthPayload,
    IAuthProvider,
    TwitchAuthException,
    UserPayload,
)


class TwitchAuthProvider(IAuthProvider):
    AUTH_SERVER = "id.twitch.tv/oauth2"
    TOKEN_ENDPOINT = f"https://{AUTH_SERVER}/token"

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri

    def authenticate_user(self, code: str) -> AuthPayload:
        payload = {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self._redirect_uri,
        }

        try:
            response = requests.post(TwitchAuthProvider.TOKEN_ENDPOINT, data=payload)
            response.raise_for_status()
            auth_data = response.json()

            id_token = auth_data.get("id_token")

            # TODO: apply token validation to check if it's actually issued by Twitch
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
                audience=self._client_id,
            )
        except InvalidTokenError as e:
            raise AuthException("Invalid token") from e

        return UserPayload(
            external_id=auth_payload["sub"],
            avatar=auth_payload["picture"],
            name=auth_payload["preferred_username"],
        )
