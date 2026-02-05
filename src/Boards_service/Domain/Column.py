from dataclasses import dataclass
from uuid import UUID

@dataclass
class Column:
    id : UUID
    name : str
    board_id : UUID
    position : int
#author_id : UUID на случай если есть пользователи