from datetime import datetime, timezone, timedelta
import jwt
from passlib.context import CryptContext

from config import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Security:
    @staticmethod
    def create_access_token(username: str, expires_delta: timedelta) -> str:
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode = {"exp": expire, "username": username}

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
