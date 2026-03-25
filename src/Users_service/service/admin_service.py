from typing import List
from uuid import UUID
from repository.interfaces.user_interface import IUserRepository
from schemas.user_schemas import UserResponse, UserUpdate
from core.exceptions import UserNotFound, ConflictError


class AdminService:
    def __init__(self, repo: IUserRepository):
        self.repo = repo


    async def get_all_users_full(self) -> List[UserResponse]:
        users = await self.repo.list_all_users()
        return [UserResponse.model_validate(u, from_attributes=True) for u in users]


    async def update_user_role(self,user_id : UUID, new_role : str) -> None:
        user = await self.repo.get_user(user_id)
        if user is None:
            raise UserNotFound('User not found')
        user.role = new_role
        await self.repo.update_user(user)

    async def delete_user(self, user_id: UUID) -> None:
        user = await self.repo.get_user(user_id)
        if not user:
            raise UserNotFound("User not found")
        await self.repo.delete_user(user_id)

    async def hard_delete_user(self, user_id: UUID) -> None:
        user = await self.repo.get_user(user_id)
        if not user:
            raise UserNotFound("User not found")
        await self.repo.hard_delete_user(user_id)


    async def update_user(self, user_id: UUID, data: UserUpdate) -> None:
        user = await self.repo.get_user(user_id)
        if not user:
            raise UserNotFound("User not found")
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
        await self.repo.update_user(user)