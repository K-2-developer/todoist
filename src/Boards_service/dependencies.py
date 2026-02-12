from Boards_service.repository.implementations.BoardRepository import BoardRepository
from src.Boards_service.service.workspace_service import WorkSpaceService
from src.Boards_service.service.board_service import  BoardService
from src.Boards_service.service.column_service import ColumnService
from src.Boards_service.service.task_service import TaskService
from src.Boards_service.Infrastructure.Database.database import get_session

def get_workspace_service() -> WorkSpaceService:
    return WorkSpaceService(repo=None)

def get_board_service( session: AsyncSession = Depends(get_session)) -> BoardService:
    board_repo = BoardRepository(session)
    workspace_repo = WorkSpaceRepository
    return BoardService(repo=None)

def get_column_service() -> ColumnService:
    return ColumnService(repo=None)

def get_task_service() -> TaskService:
    return TaskService(repo=None)