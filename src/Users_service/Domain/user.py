from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class User:
    name : str
    second_name : str
    email : str
    id : UUID
    role : str | None #вопросы есть
    password : str
    created_at : datetime
    updated_at : datetime

