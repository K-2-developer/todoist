from abc import ABC, abstractmethod
from typing import List
from src.Boards_service.schemas.task_schemas import *


class ITaskRepository(ABC):

    @abstractmethod
    async def create(self, data : TaskCreate) -> UUID:
        pass

    @abstractmethod
    async def update(self, task_id : UUID, data : TaskUpdate) -> None:
        pass

    @abstractmethod
    async def delete(self, task_id : UUID) -> None:
        pass

    @abstractmethod
    async def get(self, task_id : UUID) -> TaskResponse:
        pass

    @abstractmethod
    async def list_by_column(self, column_id : UUID) -> List[TaskNameResponse]:
        pass

    @abstractmethod
    async def exists(self, task_id : UUID) -> bool:
        pass

    @abstractmethod
    async def get_max_position(self, column_id : UUID) -> int | None:
        pass

    @abstractmethod
    async def change_position(self, task_id : UUID, new_position : int) -> TaskResponse:
        pass

    @abstractmethod
    async def move_to_column(self, task_id : UUID, column_id : UUID) -> TaskResponse:
        pass