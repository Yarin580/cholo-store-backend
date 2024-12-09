from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routes import get_current_user, get_current_admin_user
from src.api.tdo.auth_dto import LoginDto, TokenDto
from src.api.tdo.user_dto import UserCreateDto, UserResponseDto
from src.application.user.services.user import UserService
from src.modules.db import get_db_session

auth_router = APIRouter(prefix="/authentication",
                           tags=["authentication"])


@auth_router.post("/register", response_model=UserResponseDto)
async def register_user(user: UserCreateDto,
                        db_session: AsyncSession = Depends(get_db_session)):
    return await UserService(db_session).register(username=user.username,
                                  email=user.email,
                                  password=user.password,
                                  role=user.role)

@auth_router.post("/login", response_model=TokenDto)
async def login(login_data: OAuth2PasswordRequestForm = Depends(),
                db_session: AsyncSession = Depends(get_db_session)):
    return await UserService(db_session).login(username=login_data.username,
                               password=login_data.password)


@auth_router.get("/current", response_model=UserResponseDto)
async def get_current_user(user = Depends(get_current_admin_user)):
    return user
