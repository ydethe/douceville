import typing as T

from pydantic import BaseModel


class Url(BaseModel):
    url: str


class AuthorizationResponse(BaseModel):
    state: str
    code: str


class GithubUser(BaseModel):
    login: str
    name: str
    company: T.Optional[str]
    location: T.Optional[str]
    email: T.Optional[str]
    avatar_url: T.Optional[str]


class User(BaseModel):
    id: int
    login: str
    name: T.Optional[str]
    company: T.Optional[str]
    location: T.Optional[str]
    email: T.Optional[str]
    avatar_url: T.Optional[str]
    hashed_pwd: T.Optional[str]
    admin: bool
    active: bool
    stripe_id: T.Optional[str]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: User
