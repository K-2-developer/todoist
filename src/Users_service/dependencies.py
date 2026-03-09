from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Users_service.Infrastructure.Database.database import get_session
from Users_service.repository.implementations.UserRepository import UserRepository
from Users_service.service.user_service import UserService

async def get_user_service(session : AsyncSession=Depends(get_session)) -> UserService:
    repo = UserRepository(session)
    return UserService(repo)

