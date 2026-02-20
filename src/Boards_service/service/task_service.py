from typing import List

from Boards_service.Domain.Task import Task
from Boards_service.Infrastructure.Database.orm_models import task
from Boards_service.repository.interfaces.column_interface import IColumnRepository
from Boards_service.repository.interfaces.task_interface import ITaskRepository
from Boards_service.schemas.task_schemas import *


class TaskService:
    def __init__(self, task : ITaskRepository, column : IColumnRepository):
        self.task = task
        self.column = column

    async def create_task(self, task : Task) -> UUID:
        if not await self.column.exists(task.column_id):
            raise ValueError('Column not found')
        last_position = await self.task.get_max_position(task.column_id)
        task.position = (last_position or 0) + 1
        return await self.task.create(task)



    async def update_task(self, task_id : UUID, data : TaskUpdate) -> None:
        if data.title is not None:
            task.title = data.title
        if data.description is not None:
            task.description = data.description
        if data.is_archived is not None:
            task.is_archived = data.is_archived
        await self.task.update(task)


    async def delete_task(self, task_id : UUID) -> None:
       await self.task.delete(task_id)


    async def hard_delete_task(self, task_id : UUID) -> None:
        await self.task.hard_delete(task_id)

    async def get_task(self, task_id : UUID) -> Task:
        return await self.task.get(task_id)

    async def list_by_column(self, column_id : UUID) -> List[Task]:
        if not await self.column.exists(column_id):
            raise ValueError('Column not found')
        return await self.task.list_by_column(column_id)

    async def change_position(self, task_id : UUID, new_position : int) -> None:
        task = await self.task.get(task_id)
        old_position = task.position
        column_id = task.column_id
        if new_position == old_position:
            return
        await self.task.shift_positions(
            column_id=column_id,
            old_position=old_position,
            new_position=new_position
        )
        await self.task.change_position(task_id, new_position)



    async def move_to_column(self, task_id : UUID, column_id : UUID, new_position : int) -> None:
        if not await self.column.exists(column_id):
            raise ValueError('Column not found')
        await self.task.move_to_column(task_id, column_id, new_position)


