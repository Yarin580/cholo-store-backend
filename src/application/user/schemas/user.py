from pydantic import BaseModel

from src.application.user.enums import UserRoles


class UserSchema(BaseModel):
    username: str
    hashed_password: str
    role: UserRoles
    email: str

    class Config:
        from_attributes = True
