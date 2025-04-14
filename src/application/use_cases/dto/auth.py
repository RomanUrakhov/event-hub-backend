from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str
    avatar: str


class LoginAccountResult(BaseModel):
    id_token: str
    refresh_token: str
    user: User
