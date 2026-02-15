from typing import List
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from Boards_service.Domain.Column import Column
from Boards_service.Infrastructure.Database.orm_models.column import ColumnORM
from Boards_service.repository.interfaces.column_interface import IColumnRepository
from Boards_service.schemas.column_schemas import ColumnResponse


class ColumnRepository(IColumnRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, column : Column) -> UUID:
        orm = ColumnORM(
            id=column.id,
            board_id=column.board_id,
            title=column.title,
            position=column.position,
            is_archived=column.is_archived,
        )
        self.session.add(orm)
        await self.session.commit()
        return orm.id

    async def update(self, column : Column) -> None:
        stmt = select(ColumnORM).where(ColumnORM.id == column.id)
        res = await self.session.execute(stmt)
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError('Column not found')
        orm.title = column.title
        orm.position = column.position
        orm.is_archived = column.is_archived
        await self.session.commit()

    async def get(self, column_id : UUID) -> Column:
        stmt = select(ColumnORM).where(ColumnORM.id == column_id)
        res = await self.session.execute(stmt)
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError('Column not found')
        return Column(
            id=orm.id,
            title=orm.title,
            position=orm.position,
            board_id=orm.board_id,
            is_archived=orm.is_archived,
        )

    async def delete(self, column_id : UUID) -> None:
        stmt = select(ColumnORM).where(ColumnORM.id == column_id)
        res = await self.session.execute(stmt)
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError('Column not found')
        orm.is_archived = True
        await self.session.commit()

    async def hard_delete(self, column_id : UUID) -> None:
        stmt = select(ColumnORM).where(ColumnORM.id == column_id)
        res = await self.session.execute(stmt)
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError('Column not found')
        await self.session.delete(orm)
        await self.session.commit()

    async def exists(self, column_id : UUID) -> bool:
        stmt = select(ColumnORM).where(ColumnORM.id == column_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none() is not None

    async def list_by_board(self, board_id : UUID) -> List[Column]:
        stmt = select(ColumnORM).where(ColumnORM.board_id == board_id).order_by(ColumnORM.position).where(ColumnORM.is_archived == False)
        res = await self.session.execute(stmt)
        rows = res.scalars().all()
        return [
            Column(
                id=obj.id,
                title=obj.title,
                board_id=obj.board_id,
                position=obj.position,
                is_archived=obj.is_archived,
            )
            for obj in rows
        ]

    async def get_last_position(self, board_id: UUID) -> int | None:
        stmt = (
            select(func.max(ColumnORM.position))
            .where(ColumnORM.board_id == board_id)
            .where(ColumnORM.is_archived == False)
        )

        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def update_position(self, column_id: UUID, new_position: int) -> None:
        stmt = select(ColumnORM).where(ColumnORM.id == column_id)
        res = await self.session.execute(stmt)
        orm = res.scalar_one_or_none()

        if orm is None:
            raise ValueError("Column not found")

        orm.position = new_position
        await self.session.commit()

    async def shift_positions(self,board_id: UUID,new_position: int,old_position: int) -> None:
        stmt = (select(ColumnORM).where(ColumnORM.board_id == board_id).where(ColumnORM.is_archived == False))
        res = await self.session.execute(stmt)
        columns = res.scalars().all()
        if new_position < old_position:
            for col in columns:
                if new_position <= col.position < old_position:
                    col.position += 1
        elif new_position > old_position:
            for col in columns:
                if old_position < col.position <= new_position:
                    col.position -= 1
        await self.session.commit()













