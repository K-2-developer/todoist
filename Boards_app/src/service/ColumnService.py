from Boards_app.src.repository.interfaces.Column_interface import  *
from repository.interfaces.Board_interface import IBoardRepository


class ColumnService:

    def __init__(self, column : IColumnRepository, board : IBoardRepository):
        self.column = column
        self.board = board

    async def create_column(self, data : ColumnCreate) -> ColumnResponse:
        if not await self.board.exists(data.board_id):
            raise ValueError('Board not found')
        last_position = await self.column.get_last_position(data.board_id)
        data.position = (last_position or 0) + 1
        return await self.column.create(data)

    async def update_column(self, column_id : UUID, data : ColumnUpdate) -> ColumnResponse:
        if not await self.column.exists(column_id):
            raise ValueError('Column not found')
        return await self.column.update(column_id, data)

    async def delete_column(self, column_id : UUID) -> None:
        if not await self.column.exists(column_id):
            raise ValueError("Column not found")
        return await self.column.delete(column_id)

    async def get_column(self, column_id : UUID) -> ColumnResponse:
        if not await self.column.exists(column_id):
            raise ValueError('Column not found')
        return await self.column.get(column_id)

    async def list_by_board(self, board_id : UUID) -> List[ColumnResponse]:
        if not await self.board.exists(board_id):
            raise ValueError('Board not found')
        return await self.column.list_by_board(board_id)

    async def change_positions(self, column_id : UUID, new_position : int) -> ColumnResponse:
        if not await self.column.exists(column_id):
            raise ValueError('Column not found')
        column = await self.column.get(column_id)
        old_position = column.position
        if old_position == new_position:
            return column
        await self.column.shift_positions(board_id=column.board_id, old_position=old_position, new_position=new_position)
        await self.column.update_position(column_id, new_position)
        return await self.column.get(column_id)









