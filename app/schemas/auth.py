from pydantic import BaseModel


class AuthStatus(BaseModel):
    authenticated: bool
    mode: str


class AuthUser(BaseModel):
    id: str
    name: str
    email: str
    avatar_url: str | None = None
    role: str
