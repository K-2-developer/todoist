from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Board:
    id : UUID
    title : str
    workspace_id : UUID
    description : str | None
    position : int
    is_archived: bool
    created_at: datetime
    updated_at: datetime | None
    #author_id : UUID под вопросом



