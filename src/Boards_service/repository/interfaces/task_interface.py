from abc import ABC, abstractmethod
from typing import List
from Domain.Task import Task
from schemas.task_schemas import *


class ITaskRepository(ABC):

    @abstractmethod
    async def create(self, task : Task) -> UUID:
        pass

    @abstractmethod
    async def update(self, task : Task) -> None:
        pass

    @abstractmethod
    async def delete(self, task_id : UUID) -> None:
        pass

    @abstractmethod
    async def hard_delete(self, task_id : UUID) -> None:
        pass

    @abstractmethod
    async def get(self, task_id : UUID) -> Task:
        pass

    @abstractmethod
    async def list_by_column(self, column_id : UUID) -> List[Task]:
        pass

    @abstractmethod
    async def exists(self, task_id : UUID) -> bool:
        pass

    @abstractmethod
    async def get_max_position(self, column_id : UUID) -> int | None:
        pass

    @abstractmethod
    async def change_position(self, task_id : UUID, new_position : int) -> None:
        pass


    @abstractmethod
    async def shift_positions(self, column_id: UUID, old_position: int, new_position: int) -> None:
        pass

    @abstractmethod
    async def move_to_column(self, task_id: UUID, new_column_id: UUID, new_position: int) -> None:
        pass