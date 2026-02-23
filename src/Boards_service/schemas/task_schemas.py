from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class TaskCreate(BaseModel):
    title : str
    description : Optional[str] = None
    column_id : UUID


class TaskUpdate(BaseModel):
    title : Optional[str] = None
    description : Optional[str] = None
    is_archived : Optional[bool] = None
    position : Optional[int] = None


class TaskResponse(BaseModel):
    column_id: UUID
    id : UUID
    title : str
    description : Optional[str]
    created_at : datetime
    creator : Optional[str] = None
    is_archived : bool = False
    updated_at : Optional[datetime] = None
    position : int


class TaskNameResponse(BaseModel):
    title : str
    id: UUID

class TaskReorder(BaseModel):
    new_position: int

class TaskMove(BaseModel):
    new_column_id: UUID
    new_positon : int









