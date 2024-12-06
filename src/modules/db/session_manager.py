from sqlalchemy.orm import Session
from src.modules.db.database_base import SessionLocal


class SessionManager:

    def __init__(self, session: Session = None):
        if session is None:
            self._session = SessionLocal()
        else:
            self._session = session


    def __enter__(self):
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()