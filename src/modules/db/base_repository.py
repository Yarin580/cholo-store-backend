from fastapi import Depends
from sqlalchemy.future import select
from sqlalchemy.orm import Query, Session
from typing import List, Type, TypeVar, Optional, Dict, Any
from src.modules.db.base_model import Base
from .session_manager import SessionManager

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository:
    def __init__(self, model: Type[ModelType], session: Session = None):
        self.model = model
        self._session = session

    def get_db_session(self) -> SessionManager:
        try:
            return SessionManager(self._session)
        except Exception as error:
            raise Exception("Could not connect to database") from error

    def get(self, **filters) -> list[ModelType]:
        with self.get_db_session() as session:
            model_query = session.query(self.model)
            if filters:
                for attr, value in filters.items():
                    model_query = model_query.filter(getattr(self.model, attr) == value)

            model_query = model_query.all()
            if model_query:
                return model_query
            else:
                return []


    def create(self, obj_data: ModelType) -> ModelType:
        with self.get_db_session() as session:
            session.add(obj_data)
            session.commit()
            session.refresh(obj_data)
            return obj_data

    def delete(self, obj_id: int) -> None:
        with self.get_db_session() as session:
            obj = self.get(id=obj_id)[0]
            if obj:
                session.delete(obj)
                session.commit()


    def update(self, obj_data: ModelType) -> ModelType:
        with self.get_db_session() as session:
            session.add(obj_data)
            session.commit()
            session.refresh(obj_data)
            return obj_data

