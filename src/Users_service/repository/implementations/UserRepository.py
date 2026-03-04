from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from Users_service.Domain.user import User
from Users_service.Infrastructure.Database.orm_models.user import UserORM
from Users_service.repository.interfaces.user_interface import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create_user(self, user: User) -> UUID:
        orm_user = User(
            id=user.id,
            name=user.name,
            second_name=user.second_name,
            email=user.email,
            role=user.role,
            hashed_password=user.hashed_password,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active,
        )
        self.session.add(orm_user)
        await self.session.commit()
        return orm_user.id

    async def update_user(self, user: User) -> None:
        stmt = select(User).where(UserORM.id == user.id)
        res = await self.session.execute(stmt)
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError('User not found')
        orm.name = user.name
        orm.second_name = user.second_name
        orm.email = user.email
        orm.hashed_password = user.hashed_password
        orm.role = user.role
        orm.is_active = user.is_active
        await self.session.commit()

