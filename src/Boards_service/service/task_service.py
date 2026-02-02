from typing import List

from src.Boards_service.repository.interfaces.column_interface import IColumnRepository
from src.Boards_service.repository.interfaces.task_interface import ITaskRepository
from src.Boards_service.schemas.task_schemas import *


class TaskService:
    def __init__(self, task : ITaskRepository, column : IColumnRepository):
        self.task = task
        self.column = column

    async def create_task(self, data : TaskCreate) -> UUID:
        if not await self.column.exists(data.column_id):
            raise ValueError('Column not found')
        last_position = await self.task.get_max_position(data.column_id)
        data.position = (last_position or 0) + 1
        return await self.task.create(data)

    async def update_task(self, task_id : UUID, data : TaskUpdate) -> None:
        if not await self.task.exists(task_id):
            raise ValueError('Task not found')
        return await self.task.update(task_id, data)

    async def delete_task(self, task_id : UUID) -> None:
        if not await self.task.exists(task_id):
            raise ValueError('Task not found')
        return await self.task.delete(task_id)

    async def get_task(self, task_id : UUID) -> TaskResponse:
        if not await self.task.exists(task_id):
            raise ValueError('Task not found')
        return await self.task.get(task_id)

    async def list_by_column(self, column_id : UUID) -> List[TaskNameResponse]:
        if not await self.column.exists(column_id):
            raise ValueError('Column not found')
        return await self.task.list_by_column(column_id)

    async def change_position(self, task_id : UUID, new_position : int) -> TaskResponse:
        if not await self.task.exists(task_id):
            raise ValueError('Task not found')
        return await self.task.change_position(task_id, new_position)

    async def move_to_column(self, task_id : UUID, column_id : UUID) -> TaskResponse:
        if not await self.task.exists(task_id):
            raise ValueError('Task not found')
        if not await self.column.exists(column_id):
            raise ValueError('Column not found')
        return await self.task.move_to_column(task_id, column_id)

