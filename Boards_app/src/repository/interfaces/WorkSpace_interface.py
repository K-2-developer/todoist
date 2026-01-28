from abc import ABC, abstractmethod
from typing import List
from Boards_app.src.schemas.WorkSpaceSchemas import *

class IWorkSpaceRepository(ABC):

    @abstractmethod
    async def create(self, data: WorkSpaceCreate) -> WorkSpaceResponse:
        pass

    @abstractmethod
    async def update(self, workspace_id : UUID, data: WorkSpaceUpdate) -> WorkSpaceResponse:
        pass

    @abstractmethod
    async def delete(self, workspace_id : UUID) -> None:
        pass

    @abstractmethod
    async def get(self, workspace_id : UUID) -> WorkSpaceResponse:
        pass

    @abstractmethod
    async def list_all(self) -> List[OneWorkSpaceResponse]:
        pass

    @abstractmethod
    async def exists(self, workspace_id : UUID) -> bool:
        pass




