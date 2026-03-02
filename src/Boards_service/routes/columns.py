from fastapi import APIRouter, Depends
from typing import List

from Boards_service.dependencies import get_column_service
from Boards_service.schemas.column_schemas import *
from Boards_service.service.column_service import ColumnService

router = APIRouter(prefix="/columns", tags=["Columns"])

@router.post('/', response_model=UUID)
async def create_column(
        data : ColumnCreate,
        service : ColumnService = Depends(get_column_service)
):
    return await service.create_column(data)

@router.get('/{column_id}', response_model=ColumnResponse)
async def get_column(
        column_id : UUID,
        service : ColumnService = Depends(get_column_service)
):
    return await service.get_column(column_id)

@router.get('/boards/{board_id}/columns', response_model=List[ColumnNameResponse])
async def list_by_board(
        board_id : UUID,
        service : ColumnService = Depends(get_column_service)
):
    return await service.list_by_board(board_id)

@router.put('/{column_id}', response_model=ColumnResponse)
async def update_column(
        column_id : UUID,
        data : ColumnUpdate,
        service : ColumnService = Depends(get_column_service)
):
    return await service.update_column(column_id, data)

@router.delete('/{column_id}')
async def delete_column(
        column_id : UUID,
        service : ColumnService = Depends(get_column_service)
):
    await service.delete_column(column_id)
    return {'status' : 'deleted'}


@router.patch('/{column_id}', response_model=ColumnResponse)
async def reorder_column(
        column_id : UUID,
        data : ColumnReorder,
        service : ColumnService = Depends(get_column_service)
):
    return await service.change_positions(column_id, data.new_position)

