from abc import ABC, abstractmethod
from typing import List

from Boards_service.Domain.Workspace import Workspace
from src.Boards_service.schemas.workspace_schemas import *


class IWorkSpaceRepository(ABC):

    @abstractmethod
    async def create(self, data: WorkSpaceCreate) -> UUID:
        pass

    @abstractmethod
    async def update(self, workspace : Workspace) -> None:
        pass

    @abstractmethod
    async def delete(self, workspace_id : UUID) -> None:
        pass

    @abstractmethod
    async def hard_delete(self, workspace_id : UUID) -> None:
        pass

    @abstractmethod
    async def get(self, workspace_id : UUID) -> Workspace:
        pass

    @abstractmethod
    async def list_all(self) -> List[Workspace]:
        pass

    @abstractmethod
    async def exists(self, workspace_id : UUID) -> bool:
        pass




