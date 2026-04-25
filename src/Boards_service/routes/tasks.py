from fastapi import APIRouter, Depends
from typing import List
from dependencies import get_task_service
from schemas.task_schemas import *
from service.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post('/', response_model=UUID, status_code=201)
async def create_task(
        data: TaskCreate,
        service: TaskService = Depends(get_task_service)
):
    return await service.create_task(data)


@router.get('/{task_id}', response_model=TaskNameResponse, status_code=200)
async def get_task(
        task_id: UUID,
        service: TaskService = Depends(get_task_service)
):
     return service.get_task(task_id)


@router.get('/columns/{column_id}', response_model=List[TaskNameResponse], status_code=200)
async def list_by_column(
        column_id: UUID,
        service: TaskService = Depends(get_task_service)
):
    return await service.list_by_column(column_id)


@router.put('/{task_id}', status_code=204)
async def update_task(
        task_id: UUID,
        data: TaskUpdate,
        service: TaskService = Depends(get_task_service)
):
    await service.update_task(task_id, data)


@router.delete('/{task_id}', status_code=200)
async def delete_task(
        task_id: UUID,
        service: TaskService = Depends(get_task_service)
):
    await service.delete_task(task_id)
    return {"status": "archived"}

@router.delete('/{task_id}/hard', status_code=200)
async def hard_delete(
        task_id: UUID,
        service: TaskService = Depends(get_task_service)
):
    await service.hard_delete_task(task_id)
    return {"status": "deleted"}

@router.patch('/{task_id}/reorder', status_code=204)
async def reorder_task(
        task_id: UUID,
        data: TaskReorder,
        service: TaskService = Depends(get_task_service)
):
    await service.change_position(task_id, data.new_position)

@router.patch('/{task_id}/move', status_code=204)
async def move_task(
        task_id: UUID,
        data: TaskMove,
        service: TaskService = Depends(get_task_service)
):
    await service.move_to_column(task_id, data.new_column_id, data.new_position)
