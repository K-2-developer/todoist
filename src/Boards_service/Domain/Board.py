from Boards_service.repository.interfaces.board_interface import IBoardRepository
from dataclasses import dataclass
from uuid import UUID


@dataclass
class Board:
    id : UUID
    name : str
    workspace_id : UUID
    #position : int под вопросом
    #author_id : UUID под вопросом



