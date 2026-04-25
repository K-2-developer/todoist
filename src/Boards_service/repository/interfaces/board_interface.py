from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from Domain.Board import Board


class IBoardRepository(ABC):
    @abstractmethod
    async def create(self, board: Board) -> UUID:
        pass

    @abstractmethod
    async def update(self, board : Board) -> None: #(self, board_id : UUID) может и не нужен, т.к внутри Board есть id.
        pass

    @abstractmethod
    async def get(self, board_id: UUID) -> Board:
        pass

    @abstractmethod
    async def delete(self, board_id: UUID) -> None:
        pass

    @abstractmethod
    async def hard_delete(self, board_id: UUID) -> None:
        pass

    @abstractmethod
    async def list_by_workspace(self, workspace_id: UUID) -> List[Board]:
        pass

    @abstractmethod
    async def exists(self, board_id: UUID) -> bool:
        pass
