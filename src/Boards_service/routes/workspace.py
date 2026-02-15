from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List

from src.Boards_service.dependencies import get_workspace_service
from src.Boards_service.schemas.workspace_schemas import *
from src.Boards_service.service.workspace_service import WorkSpaceService

router = APIRouter(prefix="/workspace", tags=["Workspace"])

@router.post('/', response_model=UUID) #Тут вопрос по WorkspaceCreate
async def create_workspace(
        data : WorkSpaceCreate,
        service : WorkSpaceService = Depends(get_workspace_service)
):
    return await service.create_workspace(data)

@router.get('/{workspace_id}', response_model=WorkSpaceResponse)
async def get_workspace(
        workspace_id : UUID,
        service : WorkSpaceService = Depends(get_workspace_service)
):
    return await service.get_workspace(workspace_id)

@router.get('/', response_model=List[OneWorkSpaceResponse])
async def list_workspaces(
        service : WorkSpaceService = Depends(get_workspace_service)
):
    return await service.list_workspaces()

@router.put('/{workspace_id}')
async def update_workspace(
        workspace_id : UUID,
        data : WorkSpaceUpdate,
        service : WorkSpaceService = Depends(get_workspace_service)
):
    return await service.update_workspace(workspace_id, data)

@router.delete('/{workspace_id}')
async def delete_workspace(
        workspace_id : UUID,
        service : WorkSpaceService = Depends(get_workspace_service)
):
    await service.delete_workspace(workspace_id)
    return {"status" : "deleted"}


