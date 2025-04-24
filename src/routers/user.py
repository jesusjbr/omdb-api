from fastapi import APIRouter

from config import TAG_USER, API_V1
from core.deps import SessionDep
from schemas.requests.user_login_request import UserLogin
from schemas.responses.login_response import LoginResponse
from services.user_service import UserService

router = APIRouter(prefix=f"/api/{API_V1}/users")


@router.post("/login", tags=[TAG_USER])
async def login(session: SessionDep, user_login: UserLogin) -> LoginResponse:
    """
    Checks the credentials and generates a token.
    :param session: A database session
    :param user_login: Username and password to create a token.
    :return: Token
    """
    return await UserService.login(session=session, user_login=user_login)
