from apiflask import Schema
from apiflask.fields import String, Nested


class AuthWithTwitchRequestSchema(Schema):
    code = String(required=True, description="The Twitch OIDC authorization code")


class UserSchema(Schema):
    avatar = String(required=True)
    name = String(required=True)
    id = String(required=True)


class AuthWithTwitchResponseSchema(Schema):
    session_token = String(required=True)
    user = Nested(UserSchema, required=True)


class RefreshTokenResponseSchema(Schema):
    session_token = String(required=True)
