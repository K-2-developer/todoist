from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from Users_service.Domain.user import User
from core.config import settings
from Users_service.Infrastructure.Database.database import get_session
from Users_service.repository.implementations.UserRepository import UserRepository
from Users_service.service.user_service import UserService
from Users_service.schemas.user_schemas import TokenData, UserResponse

async def get_user_service(session : AsyncSession=Depends(get_session)) -> UserService:
    repo = UserRepository(session)
    return UserService(repo)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
        token : str = Depends(oauth2_scheme),
        service : UserService = Depends(get_user_service)
) -> User:
    

