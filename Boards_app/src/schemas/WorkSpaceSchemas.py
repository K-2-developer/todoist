from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from .BoardSchemas import BoardNameResponse
from datetime import datetime


class WorkSpaceCreate(BaseModel):
    name : str
    description : Optional[str] = None


class WorkSpaceUpdate(BaseModel):
    name : Optional[str] = None
    description : Optional[str] = None
    is_archived : Optional[bool] = False


class WorkSpaceResponse(BaseModel):
    id : UUID
    name : str
    description : Optional[str] = None
    board : list[BoardNameResponse]
    creator : str
    created_at : datetime
    updated_at : Optional[datetime]
    is_archived: bool = False

class OneWorkSpaceResponse(BaseModel):
    id : UUID
    name : str

