from abc import ABC, abstractmethod
from typing import List
from Boards_app.src.schemas.BoardSchemas import *


class IBoardRepository(ABC):
    @abstractmethod
    async def board_create(self, data : BoardCreate) -> BoardResponse:
        pass

    @abstractmethod
    async def board_update(self, data : BoardUpdate) -> BoardResponse:
        pass

    @abstractmethod
    async def get(self, board_id : UUID) -> BoardResponse:
        pass

    @abstractmethod
    async def delete(self, board_id : UUID) -> None:
        pass


    @abstractmethod
    async def boards_on_workspace(self, workspace_id : UUID) -> List[BoardResponse]:
        pass







