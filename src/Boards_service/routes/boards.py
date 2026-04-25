from fastapi import APIRouter, Depends
from typing import List
from dependencies import get_board_service
from schemas.board_schemas import *
from service.board_service import BoardService

router = APIRouter(prefix="/boards", tags=["Boards"])

#Разные роуты для софт и хард удаления?
@router.post("/", response_model=UUID, status_code=201)
async def create_board(
        data : BoardCreate,
        service : BoardService = Depends(get_board_service)
):
    return await service.create_board(data)

@router.get('/{board_id}', response_model=BoardResponse, status_code=200)
async def get_board(
        board_id : UUID,
        service : BoardService = Depends(get_board_service)
):
    return await service.get_board(board_id)

@router.get("/workspaces/{workspace_id}/boards", response_model=List[BoardNameResponse],status_code=200)
async def list_by_workspace(
        workspace_id : UUID,
        service : BoardService = Depends(get_board_service)
):
    return await service.list_by_workspace(workspace_id)

@router.put('/{board_id}', status_code=204)
async def update_board(
        board_id : UUID,
        data : BoardUpdate,
        service : BoardService = Depends(get_board_service)
):
     await service.update_board(board_id, data)

@router.delete('/{board_id}', status_code=200)
async def delete_board(
        board_id : UUID,
        service : BoardService = Depends(get_board_service)
):
    await service.delete_board(board_id)
    return {'status' : 'archived'}

@router.delete('/{board_id}/hard', status_code=200)
async def hard_delete(
        board_id : UUID,
        service : BoardService = Depends(get_board_service)
):
    await service.hard_delete_board(board_id)
    return {'status' : 'deleted'}
