from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class Column:
    id : UUID
    title : str
    board_id : UUID
    position : int
    is_archived : bool
    created_at: datetime
    updated_at: datetime | None
#author_id : UUID на случай если есть пользователи