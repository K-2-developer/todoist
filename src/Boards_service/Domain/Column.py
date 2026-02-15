from dataclasses import dataclass
from uuid import UUID

@dataclass
class Column:
    id : UUID
    title : str
    board_id : UUID
    position : int
    is_archived : bool
#author_id : UUID на случай если есть пользователи