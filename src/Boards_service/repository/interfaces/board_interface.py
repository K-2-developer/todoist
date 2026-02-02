from abc import ABC, abstractmethod
from typing import List
from src.Boards_service.schemas.board_schemas import *


class IBoardRepository(ABC):
    @abstractmethod
    async def create(self, data: BoardCreate) -> UUID:
        pass

    @abstractmethod
    async def update(self, board_id: UUID, data: BoardUpdate) -> None:
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
