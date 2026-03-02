from uuid import uuid4
from typing import List
from Boards_service.repository.interfaces.board_interface import IBoardRepository
from Boards_service.repository.interfaces.workspace_interface import IWorkSpaceRepository
from Boards_service.schemas.board_schemas import *
from Boards_service.Domain.Board import Board


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
            position=0,
            is_archived=False,
            created_at=datetime.now(),
            updated_at=None
        )
        return await self.board.create(board)

    async def update_board(self, board_id: UUID, data: BoardUpdate) -> None:
        board = await self.board.get(board_id)
        if data.title is not None:
            board.title = data.title
        if data.description is not None:
            board.description = data.description
        if data.is_archived is not None:
            board.is_archived = data.is_archived
        await self.board.update(board)


    async def delete_board(self, board_id: UUID) -> None:
        await self.board.delete(board_id)


    async def hard_delete_board(self, board_id: UUID) -> None:
        await self.board.hard_delete(board_id)


    async def get_board(self, board_id: UUID) -> BoardResponse: #Проверка тут не нужна, т.к get сам выбросит ошибку
        board = await self.board.get(board_id)                  #Не совсем чистая архитектура, т.к репозиторий видит Pydantic модели, но для понимания сделаю так.
        return BoardResponse(                                   #Для чистой архитектуры бизнес логика в роутах?
            id=board.id,
            title=board.title,
            description=board.description,
            workspace_id=board.workspace_id,
            position=board.position,
            is_archived=board.is_archived,
            created_at=board.created_at,
            updated_at=board.updated_at,
        )

        '''async def get_board(self, board_id: UUID) -> Board:
        return await self.board.get(board_id)   Вариант для чистой архитектуры, остальное в роуте прописать'''


    async def list_by_workspace(self, workspace_id: UUID) -> List[BoardNameResponse]:
        if not await self.workspace.exists(workspace_id):
            raise ValueError('Workspace not found')
        boards = await self.board.list_by_workspace(workspace_id)
        return [BoardNameResponse(id=obj.id, title=obj.title) for obj in boards]


#Если бизнес логика будет в роутах - тогда сервисы мало для чего нужны?