from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jwt import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from config import SECRET_KEY, ALGORITHM, AUTHORIZATION_HEADER
from repositories.database.user import UserDatabaseRepository
from repositories.database.session_factory import get_session
from schemas.shared.user import UserData

SessionDep = Annotated[AsyncSession, Depends(get_session)]
api_key_header = APIKeyHeader(name=AUTHORIZATION_HEADER)
AuthDep = Annotated[str, Depends(api_key_header)]


async def get_current_user(session: SessionDep, token: AuthDep) -> UserData:
    """
    Get the username from the payload to authenticate user.
    :param session: Database session
    :param token: Token within header Authorization
    :return: User data
    """
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await UserDatabaseRepository.get_by_username(
        session=session, username=payload["username"]
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserData.model_validate(user)


CurrentUserDep = Annotated[UserData, Depends(get_current_user)]


async def get_current_user_admin(current_user: CurrentUserDep) -> UserData:
    """
    Implements role based authorization rasising an exception for the endpoints this dependency is
    attached if the user is not admin.
    :param current_user:
    :return:
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return current_user

CurrentAdminDep = Annotated[UserData, Depends(get_current_user_admin)]