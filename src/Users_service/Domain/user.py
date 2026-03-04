from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class User:
    name : str
    second_name : str
    email : str
    id : UUID
    hashed_password : str
    role : str | None
    created_at : datetime
    updated_at : datetime | None = None
    is_active: bool = True

