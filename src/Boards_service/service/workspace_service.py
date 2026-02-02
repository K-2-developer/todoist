from uuid import UUID
from typing import List
from src.Boards_service.repository.interfaces.workspace_interface import *


class WorkSpaceService:

    def __init__(self, workspace : IWorkSpaceRepository):
        self.workspace = workspace

    async def create_workspace(self, data : WorkSpaceCreate) -> UUID:
        return await self.workspace.create(data)

    async def get_workspace(self, workspace_id : UUID) -> WorkSpaceResponse:
        return await self.workspace.get(workspace_id)

    async def update_workspace(self, workspace_id : UUID, data : WorkSpaceUpdate) -> None:
        return await self.workspace.update(workspace_id, data)

    async def delete_workspace(self, workspace_id : UUID) -> None:
        return await self.workspace.delete(workspace_id)

    async def list_workspaces(self) -> List[OneWorkSpaceResponse]:
        return await self.workspace.list_all()

