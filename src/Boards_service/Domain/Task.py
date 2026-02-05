from dataclasses import dataclass
from typing import Optional
from uuid import UUID

@dataclass
class Task:
    id : UUID
    name : str
    description : Optional[str]
    column_id : UUID
    position : int
    #author_id под вопросом

