from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

@dataclass
class Task:
    id : UUID
    title : str
    description : Optional[str]
    column_id : UUID
    position : int
    is_archived : bool
    created_at : datetime
    updated_at : datetime | None
    #author_id под вопросом

