from fastapi import HTTPException, status

from config import ACCESS_TOKEN_EXPIRE_TIME_DELTA
from core.deps import SessionDep
from core.security import Security
from repositories.database.user import UserDatabaseRepository
from repositories.database.models.user import User
from schemas.requests.user_login import UserLogin
from schemas.responses.login import LoginResponse


class UserService:
    """Service to implement business logic related with users"""

    @staticmethod
    async def login(session: SessionDep, user_login: UserLogin) -> LoginResponse:
        """
        Generates a token to authenticate in other endpoints
        :param session: A database session
        :param user_login: User data to login
        :return: Token to authenticate in other endpoints
        """

        user: User = await UserDatabaseRepository.get_by_username(
            session=session, username=user_login.username
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        credentials_are_correct = Security.verify_password(
            user_login.password, user.hashed_password
        )
        if not credentials_are_correct:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
        else:
            token = Security.create_access_token(
                username=user.username, expires_delta=ACCESS_TOKEN_EXPIRE_TIME_DELTA
            )
            return LoginResponse(token=token)
