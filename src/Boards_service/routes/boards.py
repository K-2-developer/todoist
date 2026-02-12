from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List

from src.Boards_service.dependencies import get_board_service
from src.Boards_service.schemas.board_schemas import *
from src.Boards_service.service.board_service import BoardService

router = APIRouter(prefix="/boards", tags=["Boards"])

#Разные роуты для софт и хард удаления?
@router.post("/", response_model=BoardResponse)
async def create_board(
        data : BoardCreate,
        service : BoardService = Depends(get_board_service)
):
    return await service.create_board(data)

@router.get('/{board_id}', response_model=BoardResponse)
async def get_board(
        board_id : UUID,
        service : BoardService = Depends(get_board_service)
):
    return await service.get_board(board_id)

@router.get("/workspaces/{workspace_id}/boards", response_model=List[BoardNameResponse])
async def list_by_workspace(
        workspace_id : UUID,
        service : BoardService = Depends(get_board_service)
):
    return await service.list_by_workspace(workspace_id)

@router.put('/{board_id}', response_model=BoardResponse)
async def update_board(
        board_id : UUID,
        data : BoardUpdate,
        service : BoardService = Depends(get_board_service)
):
    return await service.update_board(board_id, data)

@router.delete('/{board_id}')
async def delete_board(
        board_id : UUID,
        service : BoardService = Depends(get_board_service)
):
    await service.delete_board(board_id)
    return {"status" : "deleted"}
