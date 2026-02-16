from fastapi import APIRouter, Depends
from typing import List

from Boards_service.dependencies import get_task_service
from Boards_service.schemas.task_schemas import *
from Boards_service.service.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post('/', response_model=TaskResponse)
async def create_task(
        data: TaskCreate,
        service: TaskService = Depends(get_task_service)
):
    return await service.create_task(data)


@router.get('/{task_id}', response_model=TaskResponse)
async def get_task(
        task_id: UUID,
        service: TaskService = Depends(get_task_service)
):
    return await service.get_task(task_id)


@router.get('/columns/{column_id}', response_model=List[TaskNameResponse])
async def list_by_column(
        column_id: UUID,
        service: TaskService = Depends(get_task_service)
):
    return await service.list_by_column(column_id)


@router.put('/{task_id}', response_model=TaskResponse)
async def update_task(
        task_id: UUID,
        data: TaskUpdate,
        service: TaskService = Depends(get_task_service)
):
    return await service.update_task(task_id, data)


@router.delete('/{task_id}')
async def delete_task(
        task_id: UUID,
        service: TaskService = Depends(get_task_service)
):
    await service.delete_task(task_id)
    return {"status": "deleted"}


@router.patch('/{task_id}/reorder', response_model=TaskResponse)
async def reorder_task(
        task_id: UUID,
        data: TaskReorder,
        service: TaskService = Depends(get_task_service)
):
    return await service.change_position(task_id, data.new_position)


class TaskMove(BaseModel):
    new_column_id: UUID


@router.patch('/{task_id}/move', response_model=TaskResponse)
async def move_task(
        task_id: UUID,
        data: TaskMove,
        service: TaskService = Depends(get_task_service)
):
    return await service.move_to_column(task_id, data.new_column_id)
