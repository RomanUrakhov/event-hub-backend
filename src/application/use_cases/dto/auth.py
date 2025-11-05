from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str
    avatar: str


class LoginAccountResult(BaseModel):
    session_token: str
    user: User
