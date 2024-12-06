from datetime import timedelta, datetime, timezone
from typing import Union, Any, Optional
from src.utils import convert_to_israel_time
from config_section.config import config

from jose import jwt, JWTError

class JWTHandler:
    def __init__(self,
                 secret_key: str = None,
                 algorithm: str = None,
                 access_token_expire_minutes: int =  None):
        self.secret_key = secret_key or config.JWT_CONFIG.secret_key
        self.algorithm = algorithm or config.JWT_CONFIG.algorithm
        self.access_token_expire_minutes = access_token_expire_minutes or config.JWT_CONFIG.expires_in


    def create_token(self,
                     subject: Union[str, Any],
                     expires_delta: Optional[timedelta] = None):
        data_to_encode = {"data": subject}
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)

        expire = convert_to_israel_time(utc_time=expire)
        data_to_encode.update({"exp": expire})
        return jwt.encode(data_to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_token(self,
                     token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError as error:
            raise ValueError("Invalid or expired token " +token)


    def verify_token(self,
                     token:str) -> Union[object, None]:
        try:
            payload = self.decode_token(token)
            return payload.get("data")
        except ValueError:
            return None