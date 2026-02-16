from abc import ABC, abstractmethod
from typing import List
from Boards_service.Domain.Column import Column
from Boards_service.schemas.column_schemas import *


class IColumnRepository(ABC):
    @abstractmethod
    async def create(self, column : Column ) -> UUID: #return id
        pass

    @abstractmethod
    async def update(self, column: Column) -> None:
        pass

    @abstractmethod
    async def list_by_board(self, board_id : UUID) -> List[Column]:
        pass

    @abstractmethod
    async def get(self, column_id : UUID) -> Column:
        pass

    @abstractmethod
    async def delete(self, column_id : UUID) -> None:
        pass

    @abstractmethod
    async def hard_delete(self, column_id : UUID) -> None:
        pass

    @abstractmethod
    async def exists(self, column_id : UUID) -> bool:
        pass

#####################      DRAG & DROP     ##################

    @abstractmethod
    async def update_position(self, column_id: UUID, new_position: int) -> None:
    #Обновляет позицию конкретной колонки
        pass

    @abstractmethod
    async def get_last_position(self, board_id : UUID) -> int | None:
    #Возвращает максмальную позицию при создании колонки на борде
        pass

    @abstractmethod
    async def shift_positions(self, board_id : UUID, new_position : int, old_position : int) -> None:
    #Сдвигает позиции других колонок относительно друг друга
        pass


