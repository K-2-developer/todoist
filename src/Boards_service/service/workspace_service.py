from typing import List
from uuid import UUID, uuid4
from Boards_service.schemas.workspace_schemas import *
from Boards_service.repository.interfaces.workspace_interface import IWorkSpaceRepository
from Boards_service.Domain.Workspace import Workspace



class WorkSpaceService:

    def __init__(self, workspace : IWorkSpaceRepository):
        self.workspace = workspace

    async def create_workspace(self, data : WorkSpaceCreate) -> UUID:
        workspace = Workspace(
            id=uuid4(),
            name=data.name,
            description=data.description,
            is_archived=False
        )
        return await self.workspace.create(workspace)

    async def get_workspace(self, workspace_id : UUID) -> WorkSpaceResponse:
        workspace = await self.workspace.get(workspace_id)
        return WorkSpaceResponse(
            id=workspace.id,
            name=workspace.name,
            description=workspace.description,
            is_archived=workspace.is_archived,
            created_at=workspace.created_at,
            updated_at=workspace.updated_at
        )


    async def update_workspace(self, workspace_id : UUID, data : WorkSpaceUpdate) -> None:
        workspace = await self.workspace.get(workspace_id)
        if data.name is not None:
            workspace.name = data.name
        if data.description is not None:
            workspace.description = data.description
        if data.is_archived is not None:
            workspace.is_archived = data.is_archived
        await self.workspace.update(workspace)



    async def delete_workspace(self, workspace_id : UUID) -> None:
        await self.workspace.delete(workspace_id)


    async def hard_delete_workspace(self, workspace_id : UUID) -> None:
        await self.workspace.hard_delete(workspace_id)

    async def list_workspaces(self) -> List[OneWorkSpaceResponse]:
        workspaces = await self.workspace.list_all()
        return [OneWorkSpaceResponse(id=obj.id, name=obj.name) for obj in workspaces]

