from dataclasses import dataclass
from uuid import UUID

@dataclass
class Workspace:
    id : UUID
    name : str
    #author(owner)_id : UUID на случай если есть пользователи
