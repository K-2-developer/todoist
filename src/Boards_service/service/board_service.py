from uuid import uuid4
from typing import List
from src.Boards_service.repository.interfaces.board_interface import IBoardRepository
from src.Boards_service.repository.interfaces.workspace_interface import IWorkSpaceRepository
from src.Boards_service.schemas.board_schemas import *
from src.Boards_service.Domain.Board import Board


class BoardService:
    def __init__(self, board: IBoardRepository, workspace: IWorkSpaceRepository):
        self.board = board
        self.workspace = workspace

    async def create_board(self, data: BoardCreate) -> UUID:
        if not await self.workspace.exists(data.workspace_id):
            raise ValueError('Workspace not found')
        board = Board(
            id=uuid4(),
            title=data.title,
            description=data.description,
            workspace_id=data.workspace_id,
        )
        return await self.board.create(board)

    async def update_board(self, board_id: UUID, data: BoardUpdate) -> None:
        if not await self.board.exists(board_id):
            raise ValueError('Board not found')
        return await self.board.update(board_id, data)

    async def delete_board(self, board_id: UUID) -> None:
        if not await self.board.exists(board_id):
            raise ValueError('Board not found')
        await self.board.delete(board_id)

    async def get_board(self, board_id: UUID) -> BoardResponse:
        if not await self.board.exists(board_id):
            raise ValueError('Board not found')
        return await self.board.get(board_id)

    async def list_by_workspace(self, workspace_id: UUID) -> List[BoardNameResponse]:
        if not await self.workspace.exists(workspace_id):
            raise ValueError('Workspace not found')
        return await self.board.list_by_workspace(workspace_id)
