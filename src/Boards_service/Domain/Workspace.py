from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class Workspace:
    id : UUID
    name : str
    description : str | None
    is_archived : bool
    created_at : datetime | None = None
    updated_at : datetime | None = None
    user_id : UUID
    author_id : UUID