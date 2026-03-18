from typing import List
from uuid import UUID
from Users_service.repository.interfaces.user_interface import IUserRepository
from Users_service.schemas.user_schemas import UserResponse
from Users_service.core.exceptions import UserNotFound

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