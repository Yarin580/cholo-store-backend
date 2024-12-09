from sqlalchemy.ext.asyncio import AsyncSession

from src.application.user.enums import UserRoles
from src.application.user.models.user import User
from src.application.user.repositories.user import UserRepository
import src.modules.exceptions.base as exceptions
import bcrypt

from src.application.user.schemas.token import TokenSchema
from src.application.user.schemas.user import UserSchema
from src.modules.db.database_base import session_manager
from src.modules.jwt import JWTHandler


class UserService:

    def __init__(self, db_session:AsyncSession):
        self.user_repository = UserRepository(db_session)
        self.jwt_handler = JWTHandler()

    @staticmethod
    def _hash_password(password:str) -> str:
        """Hashes the password using bcrypt."""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    @staticmethod
    def _check_password(hashed_password:str, password:str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    async def register(self,
                 username: str,
                 password: str,
                 email:str,
                 role: UserRoles) -> UserSchema:

        user = await self.user_repository.get_by_username(username)
        if user:
            raise exceptions.DuplicateValueException("Username Already Exists")

        try:
            hashed_password = self._hash_password(password)
            user_to_create = User(username=username,
                                  hashed_password=hashed_password,
                                  email=email,
                                  role=role)
            user_created = await self.user_repository.create(obj_data=user_to_create)
            return UserSchema.model_validate(user_created)
        except Exception as error:
            raise Exception("Error registering user ," +  str(error))

    async def login(self,
              username: str,
              password: str) -> TokenSchema:

        user = await self.user_repository.get_by_username(username)
        if not user or not self._check_password(hashed_password=user.hashed_password, password=password):
            raise exceptions.UnauthorizedException("Wrong Username or Password")

        user_schema = UserSchema.model_validate(user)
        access_token = self.jwt_handler.create_token(subject={
            "username": user_schema.username,
            "email": user_schema.email,
            "role": user_schema.role.value
        })
        return TokenSchema(access_token=access_token,
                           token_type="Bearer")


    async def get_by_username(self,username: str) -> UserSchema:
        user = await self.user_repository.get_by_username(username)
        return UserSchema.model_validate(user)
