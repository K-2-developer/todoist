from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from repository.interfaces.board_interface import IBoardRepository
from Domain.Board import Board
from Infrastructure.Database.orm_models.board import BoardORM

class BoardRepository(IBoardRepository):
    def  __init__(self, session : AsyncSession):
        self.session = session

    async def create(self, board : Board) -> UUID:
        orm_board = BoardORM(
            id=board.id,
            workspace_id=board.workspace_id,
            title=board.title,
            description=board.description,
            position=board.position,
            is_archived = board.is_archived
        )
        self.session.add(orm_board)
        await self.session.commit()
        return orm_board.id

    async def update(self, board : Board) -> None:
        stmt = select(BoardORM).where(BoardORM.id == board.id)
        res = await self.session.execute(stmt)
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError('Board not found') #Проверка для безопасности, это не бизнес логика!
        orm.title = board.title
        orm.description = board.description
        orm.position = board.position
        orm.is_archived = board.is_archived
        await self.session.commit()

    async def get(self, board_id: UUID) -> Board:
        stmt = select(BoardORM).where(BoardORM.id == board_id)
        res = await self.session.execute(stmt)
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError('Board not found')
        return Board(
            id=orm.id,
            title=orm.title,
            workspace_id=orm.workspace_id,
            description=orm.description,
            position=orm.position,
            is_archived = orm.is_archived,
            created_at=orm.created_at,
            updated_at=orm.updated_at
        )


    async def delete(self, board_id: UUID) -> None:
        stmt = select(BoardORM).where(BoardORM.id == board_id)
        res = await self.session.execute(stmt)
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError("Board not found")
        orm.is_archived = True
        await self.session.commit()


    async def hard_delete(self, board_id: UUID) -> None:
        stmt = select(BoardORM).where(BoardORM.id == board_id)
        res = await self.session.execute(stmt)
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError('Board not found')
        await self.session.delete(orm)
        await self.session.commit()


    async def exists(self, board_id: UUID) -> bool:
        stmt = select(BoardORM.id).where(BoardORM.id == board_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none() is not None


    async def list_by_workspace(self, workspace_id: UUID) -> List[Board]:
        stmt = select(BoardORM).where(BoardORM.workspace_id == workspace_id).order_by(BoardORM.position).where(BoardORM.is_archived == False)
        res = await self.session.execute(stmt)
        rows = res.scalars().all()
        return [                              #потому что по контракту я должен вернуть доменную модель
            Board(
                id=obj.id,
                title=obj.title,
                description=obj.description,
                workspace_id=obj.workspace_id,
                position=obj.position,
                is_archived=obj.is_archived,
                created_at=obj.created_at,
                updated_at=obj.updated_at,
            )
            for obj in rows
        ]




