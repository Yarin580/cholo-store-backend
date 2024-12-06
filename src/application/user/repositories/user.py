from typing import Union, List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
import src.modules.exceptions.base as exceptions
from src.application.user.enums import UserRoles
from src.application.user.models.user import User
from src.modules.db.base_repository import BaseRepository


class UserRepository(BaseRepository):

    def __init__(self, session: Session = None):
        super().__init__(model=User,
                         session=session)

    def get_by_username(self, username: str) -> User:
        users = self.get(username=username)
        return None if len(users) == 0 else users[0]


    def change_user_role(self, username:str, role:UserRoles) -> User:
       user = self.get_by_username(username)
       if user is None:
           raise exceptions.NotFoundException("User not found")

       user.role = role
       self.update(user)







