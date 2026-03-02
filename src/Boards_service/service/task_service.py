from typing import List
from uuid import uuid4

from Boards_service.Domain.Task import Task
from Boards_service.repository.interfaces.column_interface import IColumnRepository
from Boards_service.repository.interfaces.task_interface import ITaskRepository
from Boards_service.schemas.task_schemas import *


class TaskService:
    def __init__(self, task : ITaskRepository, column : IColumnRepository):
        self.task = task
        self.column = column

    async def create_task(self, data : TaskCreate) -> UUID:
        if not await self.column.exists(data.column_id):
            raise ValueError('Column not found')
        last_position = await self.task.get_max_position(data.column_id)
        data.position = (last_position or 0) + 1
        task = Task(
            id=uuid4(),
            title=data.title,
            description=data.description,
            column_id=data.column_id,
            position=data.position,
            is_archived=False
        )
        id = await self.task.create(task)
        return id



    async def update_task(self, task_id : UUID, data : TaskUpdate) -> None:
        task = await self.task.get(task_id)
        if data.title is not None:
            task.title = data.title
        if data.description is not None:
            task.description = data.description
        if data.is_archived is not None:
            task.is_archived = data.is_archived
        if data.position is not None:
            task.position = data.position
        await self.task.update(task)


    async def delete_task(self, task_id : UUID) -> None:
       await self.task.delete(task_id)


    async def hard_delete_task(self, task_id : UUID) -> None:
        await self.task.hard_delete(task_id)

    async def get_task(self, task_id : UUID) -> TaskNameResponse:
        task = await self.task.get(task_id)
        return TaskNameResponse(
            title=task.title,
            id=task.id,
        )

    async def list_by_column(self, column_id : UUID) -> List[TaskNameResponse]:
        if not await self.column.exists(column_id):
            raise ValueError('Column not found')
        tasks= await self.task.list_by_column(column_id)
        return [TaskNameResponse(
            id=t.id,
            title=t.title,
        )for t in tasks]


    async def change_position(self, task_id : UUID, new_position : int) -> None:
        task = await self.task.get(task_id)
        old_position = task.position
        column_id = task.column_id
        if new_position == old_position:
            return
        max_position = await self.task.get_max_position(column_id)
        if max_position is None:
            return
        if new_position < 1:
            new_position = 1
        if new_position > max_position:
            new_position = max_position
        if new_position == old_position:
            return
        await self.task.shift_positions(column_id, old_position ,new_position)
        await self.task.change_position(task_id, new_position)




    async def move_to_column(self, task_id : UUID, new_column_id : UUID, new_position : int) -> None:
        if not await self.column.exists(new_column_id):
            raise ValueError('Column not found')
        task = await self.column.get(task_id)
        if task.column_id == new_column_id:
            await self.task.change_position(task_id, new_position)
            return
        max_position = await self.task.get_max_position(new_column_id)
        max_position = max_position or 0
        if new_position < 1:
            new_positon = 1
        if new_position > max_position:
            new_position = max_position
        await self.task.move_to_column(task_id, new_column_id, new_position)


