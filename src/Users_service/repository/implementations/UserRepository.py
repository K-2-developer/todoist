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
        orm_user = UserORM(
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
        stmt = select(UserORM).where(UserORM.id == user.id)
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

    async def hard_delete_user(self, user_id : UUID) -> None:
        stmt = select(UserORM).where(UserORM.id == user_id)
        res = await self.session.execute(stmt)
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError('User not found')
        await self.session.delete(orm)
        await self.session.commit()

    async def delete_user(self, user_id : UUID) -> None:
        stmt = select(UserORM).where(UserORM.id == user_id)
        res = await self.session.execute(stmt)
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError('User not found')
        orm.is_active = False
        await self.session.commit()


    async def get_user(self, user_id : UUID) -> User:
        stmt = select(UserORM).where(UserORM.id == user_id)
        res = await self.session.execute(stmt)
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError('User not found')
        return User(
            id=orm.id,
            name=orm.name,
            second_name=orm.second_name,
            email=orm.email,
            hashed_password=orm.hashed_password,
            role=orm.role,
            is_active=orm.is_active,
            created_at=orm.created_at,
            updated_at=orm.updated_at
        )

    async def list_all_users(self) -> List[User]:
        stmt = select(UserORM).where(UserORM.is_active == True).order_by(UserORM.created_at)
        res = await self.session.execute(stmt)
        rows = res.scalars().all()
        return [
            User(
                id=obj.id,
                name=obj.name,
                second_name=obj.second_name,
                email=obj.email,
                hashed_password=obj.hashed_password,
                role=obj.role,
                is_active=obj.is_active,
                created_at=obj.created_at,
                updated_at=obj.updated_at
            )
            for obj in rows
        ]

    async def get_user_by_email(self, email : str) -> User:
        stmt = select(UserORM).where(UserORM.email == email)
        res = await self.session.execute(stmt)
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError('User not found')
        return User(
            id=orm.id,
            name=orm.name,
            second_name=orm.second_name,
            email=orm.email,
            hashed_password=orm.hashed_password,
            role=orm.role,
            is_active=orm.is_active,
            created_at=orm.created_at,
            updated_at=orm.updated_at
        )







