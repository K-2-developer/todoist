from typing import List
from uuid import UUID
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from Domain.Task import Task
from Infrastructure.Database.orm_models.task import TaskORM
from repository.interfaces.task_interface import ITaskRepository


class TaskRepository(ITaskRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task: Task) -> UUID:
        orm = TaskORM(
            id=task.id,
            column_id=task.column_id,
            title=task.title,
            description=task.description,
            position=task.position,
            is_archived=task.is_archived,
        )
        self.session.add(orm)
        await self.session.commit()
        return orm.id

    async def update(self, task: Task) -> None:
        stmt = select(TaskORM).where(TaskORM.id == task.id)
        res = await self.session.execute(stmt)
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError('Task not found')
        orm.title = task.title
        orm.description = task.description
        orm.position = task.position
        orm.is_archived = task.is_archived
        await self.session.commit()

    async def delete(self, task_id: UUID) -> None:
        res = await self.session.execute(select(TaskORM).where(TaskORM.id == task_id))
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError("Task not found")
        deleted_position = orm.position
        column_id = orm.column_id
        orm.is_archived = True
        shifted = (
            update(TaskORM)
            .where(
                TaskORM.column_id == column_id,
                TaskORM.is_archived == False,
                TaskORM.position > deleted_position,
            )
            .values(position=TaskORM.position - 1))
        await self.session.execute(shifted)
        await self.session.commit()

    async def hard_delete(self, task_id: UUID) -> None:
        res = await self.session.execute(select(TaskORM).where(TaskORM.id == task_id))
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError("Task not found")
        deleted_position = orm.position
        column_id = orm.column_id
        await self.session.delete(orm)
        shifted = (
            update(TaskORM)
            .where(
                TaskORM.column_id == column_id,
                TaskORM.is_archived == False,
                TaskORM.position > deleted_position,
            )
            .values(position=TaskORM.position - 1)
        )
        await self.session.execute(shifted)
        await self.session.commit()

    async def get(self, task_id: UUID) -> Task:
        stmt = select(TaskORM).where(TaskORM.id == task_id)
        res = await self.session.execute(stmt)
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError('Task not found')
        return Task(
            id=orm.id,
            column_id=orm.column_id,
            title=orm.title,
            description=orm.description,
            position=orm.position,
            is_archived=orm.is_archived,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    async def list_by_column(self, column_id: UUID) -> List[Task]:
        stmt =(
            select(TaskORM)
             .where(TaskORM.column_id == column_id)
             .order_by(TaskORM.position)
             .where(TaskORM.is_archived == False))
        res = await self.session.execute(stmt)
        rows = res.scalars().all()
        return [Task(
            id=obj.id,
            title=obj.title,
            description=obj.description,
            position=obj.position,
            column_id=obj.column_id,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
            is_archived=obj.is_archived
        )
            for obj in rows
        ]

    async def exists(self, task_id: UUID) -> bool:
        stmt = select(TaskORM.id).where(TaskORM.id == task_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none() is not None

    async def get_max_position(self, column_id: UUID) -> int | None:
        stmt = select(func.max(TaskORM.position)).where(TaskORM.column_id == column_id, TaskORM.is_archived == False)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def change_position(self, task_id: UUID, new_position: int) -> None: #Меняет позицию одной колонки
        stmt = select(TaskORM).where(TaskORM.id == task_id)
        res = await self.session.execute(stmt)
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError('Task not found')
        orm.position = new_position
        await self.session.commit()

    async def shift_positions(self, column_id: UUID, old_position: int, new_position: int) -> None: #Двигает оставшиеся колонки, чтобы не было дырок
        if new_position > old_position:
            stmt = (
                update(TaskORM)
                .where(
                    TaskORM.column_id == column_id,
                    TaskORM.is_archived == False,
                    TaskORM.position > old_position,
                    TaskORM.position <= new_position,
                )
                .values(position=TaskORM.position - 1)
            )
        else:
            stmt = (
                update(TaskORM)
                .where(
                    TaskORM.column_id == column_id,
                    TaskORM.is_archived == False,
                    TaskORM.position < old_position,
                    TaskORM.position >= new_position,
                )
                .values(position=TaskORM.position + 1)
            )
        await self.session.execute(stmt)
        await self.session.commit()

    async def move_to_column(self, task_id: UUID, new_column_id: UUID, new_position: int) -> None:
        res = await self.session.execute(select(TaskORM).where(TaskORM.id == task_id))
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError("Task not found")
        old_column_id = orm.column_id
        old_position = orm.position
        shift_old = (
            update(TaskORM)
            .where(
                TaskORM.column_id == old_column_id,
                TaskORM.is_archived == False,
                TaskORM.position > old_position,
            )
            .values(position=TaskORM.position - 1)
        )
        await self.session.execute(shift_old)
        shift_new = (
            update(TaskORM)
            .where(
                TaskORM.column_id == new_column_id,
                TaskORM.is_archived == False,
                TaskORM.position >= new_position,
            )
            .values(position=TaskORM.position + 1)
        )
        await self.session.execute(shift_new)
        orm.column_id = new_column_id
        orm.position = new_position
        await self.session.commit()

