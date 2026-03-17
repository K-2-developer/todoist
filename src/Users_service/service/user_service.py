from typing import List
from uuid import uuid4, UUID
from pwdlib import PasswordHash
from Users_service.Domain.user import User
from Users_service.repository.interfaces.user_interface import IUserRepository
from Users_service.schemas.user_schemas import UserCreate, UserUpdate, UserResponse, UserResponseShort, UserEmailResponse
from jose import jwt
from Users_service.core.config import settings
from datetime import datetime, timedelta, timezone
from Users_service.core.exceptions import UserNotFound, PermissionError, ConflictError

hasher = PasswordHash.recommended()

class UserService:
    def __init__(self, repo : IUserRepository):
        self.repo = repo

    def create_access_token(self, data : dict, expires_delta : timedelta | None=None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode.update({'exp' : expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt

    async def authenticate_user(self, email : str, password : str) -> User | None:
        user = await self.repo.get_user_by_email(email)
        if user is None:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user



    def hash_password(self, password : str) -> str:
        return hasher.hash(password)

    def verify_password(self, password : str, hashed_password : str) -> bool:
        return hasher.verify(password, hashed_password)

    async def create_user(self, data : UserCreate) -> UUID:
        existing_user = await self.repo.get_user_by_email(data.email)
        if existing_user:
            raise ConflictError('Email already registered')
        hashed_password = self.hash_password(data.password)
        user = User(
            id=uuid4(),
            email=data.email,
            name=data.name,
            second_name=data.second_name,
            hashed_password=hashed_password,
            is_active=True,
            created_at=datetime.now(),
            updated_at=None,
            role='user'
        )
        await self.repo.create_user(user)
        return user.id


    async def update_user(self, user_id : UUID, data : UserUpdate, current_user : User) -> None:
        user = await self.repo.get_user(user_id)
        if user is None:
            raise UserNotFound("User not found")
        if current_user.id != user.id:
            raise PermissionError('Not enough permissions')
        if data.name is not None:
            user.name = data.name
        if data.second_name is not None:
            user.second_name = data.second_name
        if data.email is not None and data.email != user.email:
            existing = await self.repo.get_user_by_email(data.email)
            if existing and existing.id != user_id:
                raise ConflictError("Email already in use")
            user.email = data.email
        if data.role is not None:
            user.role = data.role
        if data.is_active is not None:
            user.is_active = data.is_active
        if data.password is not None:
            user.hashed_password = self.hash_password(data.password)

        user.updated_at = datetime.now()
        await self.repo.update_user(user)


    async def get_user(self, user_id : UUID, current_user : User) -> UserResponse:
        user = await self.repo.get_user(user_id)
        if user is None:
            raise UserNotFound('User not found')
        if current_user.id != user.id:
            raise PermissionError('Not enough permissions')
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            second_name=user.second_name,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    async def delete_user(self, user_id : UUID, current_user : User) -> None:
        user = await self.repo.get_user(user_id)
        if user is None:
            raise UserNotFound('User not found')
        if current_user.id != user.id:
            raise PermissionError('Not enough permissions')
        await self.repo.delete_user(user_id)


    async def hard_delete_user(self, user_id : UUID, current_user : User) -> None:
        user = await self.repo.get_user(user_id)
        if user is None:
            raise UserNotFound('User not found')
        if current_user.id != user.id:
            raise PermissionError('Not enough permissions')
        await self.repo.hard_delete_user(user_id)

    async def list_all_users(self) -> List[UserResponseShort]:
        users = await self.repo.list_all_users()
        return [UserResponseShort(
            id=u.id,
            email=u.email,
            name=u.name,
            second_name=u.second_name,
            role=u.role
        ) for u in users]

    async def get_user_by_email(self, email : str) -> UserEmailResponse:
        user = await self.repo.get_user_by_email(email)
        if user is None:
            raise UserNotFound('User not found')
        return UserEmailResponse(
            name=user.name,
            second_name=user.second_name,
            email=user.email
        )








