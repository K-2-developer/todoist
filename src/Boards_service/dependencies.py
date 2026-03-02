from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Boards_service.repository.implementations.BoardRepository import BoardRepository
from Boards_service.repository.implementations.ColumnRepository import ColumnRepository
from Boards_service.repository.implementations.TaskRepository import TaskRepository
from Boards_service.repository.implementations.WorkspaceRepository import WorkspaceRepository
from Boards_service.service.workspace_service import WorkSpaceService
from Boards_service.service.board_service import  BoardService
from Boards_service.service.column_service import ColumnService
from Boards_service.service.task_service import TaskService
from Boards_service.Infrastructure.Database.database import get_session

def get_workspace_service(session : AsyncSession = Depends(get_session)) -> WorkSpaceService:
    workspace_repo = WorkspaceRepository(session)
    return WorkSpaceService(workspace_repo)

def get_board_service( session: AsyncSession = Depends(get_session)) -> BoardService:
    board_repo = BoardRepository(session)
    workspace_repo = WorkspaceRepository(session)
    column_repo = ColumnRepository(session)
    return BoardService(board_repo, workspace_repo, column_repo)

def get_column_service(session: AsyncSession = Depends(get_session)) -> ColumnService:
    column_repo = ColumnRepository(session)
    board_repo = BoardRepository(session)
    return ColumnService(column_repo, board_repo)


def get_task_service(session : AsyncSession = Depends(get_session)) -> TaskService:
    task_repo = TaskRepository(session)
    column_repo = ColumnRepository(session)
    return TaskService(task_repo, column_repo)
