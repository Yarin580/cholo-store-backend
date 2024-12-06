from pydantic import BaseModel


class TokenDto(BaseModel):
    access_token: str
    token_type: str


class LoginDto(BaseModel):
    username: str
    password: str