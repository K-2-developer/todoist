from datetime import datetime
from typing import List, Optional
from uuid import uuid4, UUID
from pwdlib import PasswordHash
from pydantic import ValidationError

from Users_service.Domain.user import User
from Users_service.repository.interfaces.user_interface import IUserRepository
from Users_service.schemas.user_schemas import UserCreate, UserUpdate, UserResponse

hashed_pass = PasswordHash.reccomended()

class UserService:
    def __init__(self, repo : IUserRepository):
        self.repo = repo

    def hashed_pass(self, password : str) -> str:
        return hashed_pass.hash(password)

    def verify_password(self, password : str, hashed_password : str) -> bool:
        return hashed_password.verify(password, hashed_password)

    async def create_user(self, data : UserCreate) -> UUID:
        existing_user = await self.repo.get_user_by_email(data.email)
        if existing_user:
            raise ValueError('Email already registered')
        hashed_password = self.hashed_pass(data.password)
        user = User(
            id=uuid4(),
            email=data.email,
            name=data.name,
            second_name=data.second_name,
            hashed_password=hashed_password,
            role=data.role or "user",
            is_active=True,
            created_at=datetime.now(),
            updated_at=None
        )
        await self.repo.create_user(user)
        return user.id


    async def update_user(self, user_id : UUID, data : UserUpdate) -> None:
        user = await self.repo.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        if data.name is not None:
            user.name = data.name
        if data.second_name is not None:
            user.second_name = data.second_name
        if data.email is not None and data.email != user.email:
            existing = await self.repo.get_user_by_email(data.email)
            if existing and existing.id != user_id:
                raise ValueError("Email already in use")
            user.email = data.email
        if data.role is not None:
            user.role = data.role
        if data.is_active is not None:
            user.is_active = data.is_active
        if data.password is not None:
            user.hashed_password = self._hash_password(data.password)

        user.updated_at = datetime.now()
        await self.repo.update_user(user)


    async def get_user(self, user_id : UUID) -> UserResponse:
        user = await self.repo.get_user(user_id)
        if user is None:
            raise ValueError('User not found')
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
    async def delete_user(self, user_id : UUID) -> None:
        await self.repo.delete_user(user_id)

    async def hard_delete_user(self, user_id : UUID) -> None:
        await self.repo.hard_delete_user(user_id)

    




