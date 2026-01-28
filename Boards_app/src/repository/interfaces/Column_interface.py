from abc import ABC, abstractmethod
from typing import List
from Boards_app.src.schemas.ColumnSchemas import *


class IColumnRepository(ABC):
    @abstractmethod
    async def create(self, data: ColumnCreate) -> ColumnResponse:
        pass

    @abstractmethod
    async def update(self, column_id : UUID, data: ColumnUpdate) -> ColumnResponse:
        pass

    @abstractmethod
    async def list_by_board(self, board_id : UUID) -> List[ColumnResponse]:
        pass

    @abstractmethod
    async def count_in_board(self, board_id: UUID) -> int:
        pass

    @abstractmethod
    async def get(self, column_id : UUID) -> ColumnResponse:
        pass

    @abstractmethod
    async def change_position(self, column_id : UUID, new_position : int) -> ColumnResponse:
        pass

    @abstractmethod
    async def delete(self, column_id : UUID) -> None:
        pass

    @abstractmethod
    async def exists(self, column_id : UUID) -> bool:
        pass
    
    @abstractmethod
    async def get_max_position(self, board_id : UUID) -> int:
        pass


