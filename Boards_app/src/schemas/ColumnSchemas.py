from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from .TaskSchemas import TaskNameResponse


class ColumnCreate(BaseModel):
    title : str
    board_id : UUID


class ColumnUpdate(BaseModel):
    title : Optional[str] = None
    position: Optional[int] = None  # пригодится для drag & drop.
    is_archived : Optional[bool] = False


class ColumnResponse(BaseModel):
    board_id : UUID
    id : UUID
    title : str
    tasks : list[TaskNameResponse] #для вывода названий задач
    creator : str
    created_at : datetime
    updated_at : Optional[datetime] = None
    position: int  # пригодится для drag & drop.
    is_archived : bool = False