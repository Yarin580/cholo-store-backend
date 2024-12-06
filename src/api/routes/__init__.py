from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from src.api.tdo.user_dto import UserResponseDto
from src.application.user.enums import UserRoles
from src.application.user.services.user import UserService
from src.modules.jwt import JWTHandler

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authentication/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponseDto:
    """Retrieve the current user from the token."""
    jwt_handler = JWTHandler()
    user_payload = jwt_handler.verify_token(token)
    if user_payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_service = UserService()
    user = user_service.get_by_username(username=user_payload.get("username"))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return UserResponseDto(username=user.username,
                           email=user.email,
                           role=user.role)


def get_current_admin_user(token=Depends(oauth2_scheme)) -> UserResponseDto:
    current_user = get_current_user(token=token)
    if current_user.role != UserRoles.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid or expired token",
                            headers={"WWW-Authenticate": "Bearer"})

    return current_user



