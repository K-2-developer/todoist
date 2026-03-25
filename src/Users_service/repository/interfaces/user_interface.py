from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from Domain.user import User

class IUserRepository(ABC):
    @abstractmethod
    async def create_user(self, user : User) -> UUID:
        pass

    @abstractmethod
    async def update_user(self, user : User) -> None:
        pass

    @abstractmethod
    async def hard_delete_user(self, user_id : UUID) -> None:
        pass

    @abstractmethod
    async def delete_user(self, user_id : UUID) -> None:
        pass


    @abstractmethod
    async def get_user(self, user_id : UUID) -> User:
        pass


    @abstractmethod
    async def list_all_users(self) -> List[User]:
        pass


    # @abstractmethod
    # async def get_user_by_id(self, user_id : UUID) -> UUID:
    #     pass


    @abstractmethod
    async def get_user_by_email(self, email: str) -> User:
        pass
