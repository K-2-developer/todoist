from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from Users_service.Domain.user import User

class IUserRepository(ABC):
    @abstractmethod
    async def create_user(self, user : User) -> UUID:
        pass

    @abstractmethod
    async def update_user(self, user : User) -> None:
        pass

    async def delete_user(self, user : User) -> None:
        pass

    async def get_user(self, user : User) -> UUID:
        pass

    async def list_all_users(self, data : List[User]) -> List[User]:
        pass

    async def get_user_by_id(self, user_id : UUID) -> UUID:
        pass

    async def list_users_by_boards(self): #Тут вопросы
        pass

