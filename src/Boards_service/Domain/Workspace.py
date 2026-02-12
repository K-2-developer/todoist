from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class Workspace:
    id : UUID
    name : str
    description : str | None
    is_archived : bool
    created_at : datetime
    updated_at : datetime | None
    #user_id : UUID
    #author(owner)_id : UUID на случай если есть пользователи
