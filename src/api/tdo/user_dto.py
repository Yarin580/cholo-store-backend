from pydantic import BaseModel

from src.application.user.enums import UserRoles


class UserCreateDto(BaseModel):
    username: str
    password: str
    email: str
    role: UserRoles = UserRoles.USER


class UserResponseDto(BaseModel):
    username: str
    email: str
    role: UserRoles