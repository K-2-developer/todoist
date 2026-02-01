from abc import ABC, abstractmethod
from typing import List
from Boards_app.src.schemas.BoardSchemas import *


class IBoardRepository(ABC):
    @abstractmethod
    async def create(self, data: BoardCreate) -> BoardResponse:
        pass

    @abstractmethod
    async def update(self, board_id: UUID, data: BoardUpdate) -> BoardResponse:
        pass

    @abstractmethod
    async def get(self, board_id: UUID) -> BoardResponse:
        pass

    @abstractmethod
    async def delete(self, board_id: UUID) -> None:
        pass

    @abstractmethod
    async def list_by_workspace(self, workspace_id: UUID) -> List[BoardNameResponse]:
        pass

    @abstractmethod
    async def exists(self, board_id: UUID) -> bool:
        pass
