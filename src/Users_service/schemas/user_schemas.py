from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name : str
    second_name : str
    email : EmailStr
    password : str


class UserUpdate(BaseModel):
    name : Optional[str] = None
    second_name : Optional[str] = None
    email : Optional[EmailStr] = None
    role : Optional[str] = None
    is_active : Optional[bool] = None
    password: Optional[str] = None



class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    second_name: str
    role: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserLogin(BaseModel):
    username : str
    password : str

class UserResponseShort(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    second_name: str
    role : Optional[str] = None

class UserEmailResponse(BaseModel):
    name : Optional[str]
    second_name : Optional[str]
    email : EmailStr