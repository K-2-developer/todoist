from fastapi import APIRouter, Depends
from typing import List
from Boards_service.dependencies import get_workspace_service
from Boards_service.schemas.workspace_schemas import *
from Boards_service.service.workspace_service import WorkSpaceService

router = APIRouter(prefix="/workspace", tags=["Workspace"])

@router.post('/', response_model=UUID, status_code=201)
async def create_workspace(
        data : WorkSpaceCreate,
        service : WorkSpaceService = Depends(get_workspace_service)
):
    return await service.create_workspace(data)

@router.get('/{workspace_id}', response_model=WorkSpaceResponse, status_code=200)
async def get_workspace(
        workspace_id : UUID,
        service : WorkSpaceService = Depends(get_workspace_service)
):
    return await service.get_workspace(workspace_id)

@router.get('/', response_model=List[OneWorkSpaceResponse], status_code=200)
async def list_workspaces(
        service : WorkSpaceService = Depends(get_workspace_service)
):
    return await service.list_workspaces()

@router.put('/{workspace_id}', status_code=204)
async def update_workspace(
        workspace_id : UUID,
        data : WorkSpaceUpdate,
        service : WorkSpaceService = Depends(get_workspace_service)
):
    await service.update_workspace(workspace_id, data)

@router.delete('/{workspace_id}', status_code=200)
async def delete_workspace(
        workspace_id : UUID,
        service : WorkSpaceService = Depends(get_workspace_service)
):
    await service.delete_workspace(workspace_id)
    return {'status' : 'archived'}

@router.delete('/{workspace_id}/hard', status_code=200)
async def hard_delete_workspace(
        workspace_id : UUID,
        service : WorkSpaceService = Depends(get_workspace_service)
):
    await service.hard_delete_workspace(workspace_id)
    return {'status' : 'deleted'}




