from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from .column_schemas import ColumnResponse


class BoardCreate(BaseModel):
    title: str
    description: Optional[str] = None
    workspace_id: UUID


class BoardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_archived: Optional[bool] = False


class BoardResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    workspace_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    position: int  # пригодится для сортировки на случай нескольких бордов в одном рабочем пространстве
    creator: str
    columns: list[ColumnResponse]
    is_archived: bool = False


class BoardNameResponse(BaseModel):
    title: str
    id: UUID
