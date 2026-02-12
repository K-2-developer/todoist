from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from .board_schemas import BoardNameResponse
from datetime import datetime


class WorkSpaceCreate(BaseModel):
    name : str
    description : Optional[str] = None


class WorkSpaceUpdate(BaseModel):
    name : Optional[str] = None
    description : Optional[str] = None
    is_archived : Optional[bool] = None


class WorkSpaceResponse(BaseModel):
    id : UUID
    name : str
    description : Optional[str] = None
    board : list[BoardNameResponse] = [] #тоже заглушка
    #creator_id : Optional[UUID] = None #заглушка.переделать когда будет юзер сервис
    created_at : datetime
    updated_at : Optional[datetime]
    is_archived: bool = False

class OneWorkSpaceResponse(BaseModel):
    id : UUID
    name : str

