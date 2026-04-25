from fastapi import APIRouter, Depends
from typing import List

from dependencies import get_column_service
from schemas.column_schemas import *
from service.column_service import ColumnService

router = APIRouter(prefix="/columns", tags=["Columns"])

@router.post('/', response_model=UUID, status_code=201)
async def create_column(
        data : ColumnCreate,
        service : ColumnService = Depends(get_column_service)
):
    return await service.create_column(data)

@router.get('/{column_id}', response_model=ColumnResponse, status_code=200)
async def get_column(
        column_id : UUID,
        service : ColumnService = Depends(get_column_service)
):
    return await service.get_column(column_id)

@router.get('/boards/{board_id}/columns', response_model=List[ColumnNameResponse], status_code=200)
async def list_by_board(
        board_id : UUID,
        service : ColumnService = Depends(get_column_service)
):
    return await service.list_by_board(board_id)

@router.put('/{column_id}', status_code=204)
async def update_column(
        column_id : UUID,
        data : ColumnUpdate,
        service : ColumnService = Depends(get_column_service)
):
    await service.update_column(column_id, data)

@router.delete('/{column_id}', status_code=200)
async def delete_column(
        column_id : UUID,
        service : ColumnService = Depends(get_column_service)
):
    await service.delete_column(column_id)
    return {'status' : 'archived'}

@router.delete('/{column_id}/hard', status_code=200)
async def hard_delete(
        column_id : UUID,
        service : ColumnService = Depends(get_column_service)
):
    await service.hard_delete(column_id)
    return {'status' : 'deleted'}

@router.patch('/{column_id}',status_code=204)
async def reorder_column(
        column_id : UUID,
        data : ColumnReorder,
        service : ColumnService = Depends(get_column_service)
):
     await service.change_positions(column_id, data.new_position)

