from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from Users_service.service.admin_service import AdminService
from core.config import settings
from Users_service.Infrastructure.Database.database import get_session
from Users_service.repository.implementations.UserRepository import UserRepository
from Users_service.service.user_service import UserService
from Users_service.Domain.user import User


async def get_user_service(session : AsyncSession=Depends(get_session)) -> UserService:
    repo = UserRepository(session)
    return UserService(repo)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_admin_service(session: AsyncSession = Depends(get_session)) -> AdminService:
    repo = UserRepository(session)
    return AdminService(repo)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await service.get_user_domain(UUID(user_id))
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_admin_user(
        current_user : User = Depends(get_current_user)
) -> User:
    if current_user.role != 'admin':
        raise PermissionError('For admin use only')
    else:
        return current_user
