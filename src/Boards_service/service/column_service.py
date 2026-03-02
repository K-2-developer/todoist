from uuid import uuid4
from Boards_service.Domain.Column import Column
from Boards_service.repository.interfaces.board_interface import IBoardRepository
from Boards_service.repository.interfaces.column_interface import IColumnRepository
from Boards_service.schemas.column_schemas import *
from typing import List


class ColumnService:

    def __init__(self, column : IColumnRepository, board : IBoardRepository):
        self.column = column
        self.board = board

    async def create_column(self, data : ColumnCreate) -> UUID:
        if not await self.board.exists(data.board_id):
            raise ValueError('Board not found')
        last_position = await self.column.get_last_position(data.board_id)
        new_position = (last_position or 0) + 1
        column = Column(
            id=uuid4(),
            title=data.title,
            board_id=data.board_id,
            position=new_position,
            is_archived=False,
            created_at=datetime.now(),
            updated_at=None
        )
        return await self.column.create(column)

    async def update_column(self, column_id : UUID, data : ColumnUpdate) -> None:
        column = await self.column.get(column_id)
        if data.title is not None:
            column.title = data.title
        if data.position is not None:
            column.position = data.position
        if data.is_archived is not None:
            column.is_archived = data.is_archived
        await self.column.update(column)



    async def delete_column(self, column_id : UUID) -> None:
        return await self.column.delete(column_id)

    async  def hard_delete(self, column_id : UUID) -> None:
        return await self.column.hard_delete(column_id)

    async def get_column(self, column_id : UUID) -> ColumnResponse:
        column = await self.column.get(column_id)

        return ColumnResponse(
            id=column.id,
            title=column.title,
            board_id=column.board_id,
            position=column.position,
            is_archived=column.is_archived,
            created_at=column.created_at,
            updated_at=column.updated_at
        )

    async def list_by_board(self, board_id : UUID) -> List[ColumnNameResponse]:
        columns = await self.column.list_by_board(board_id)
        return [ColumnNameResponse(id=c.id, title=c.title) for c in columns]


    async def change_positions(self, column_id : UUID, new_position : int) -> None:
        column = await self.column.get(column_id)
        old_position = column.position
        if old_position == new_position:
            return
        await self.column.shift_positions(board_id=column.board_id, old_position=old_position, new_position=new_position)
        await self.column.update_position(column_id, new_position)









