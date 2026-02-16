from typing import List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from Boards_service.Domain.Workspace import Workspace
from Boards_service.Infrastructure.Database.orm_models.workspace import WorkspaceORM
from Boards_service.repository.interfaces.workspace_interface import IWorkSpaceRepository

class WorkspaceRepository(IWorkSpaceRepository):
    def __init__(self, session : AsyncSession):
        self.session = session

    async def create(self, workspace : Workspace) -> UUID:
        orm = WorkspaceORM(
            id = workspace.id,
            name = workspace.name,
            description = workspace.description,
            is_archived = workspace.is_archived,
        )
        self.session.add(orm)
        await self.session.commit()
        return orm.id

    async def update(self, workspace : Workspace) -> None:
        stmt = select(WorkspaceORM).where(WorkspaceORM.id == workspace.id)
        res = await self.session.execute(stmt)
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError("Workspace not found")
        orm.name = workspace.name
        orm.description = workspace.description
        orm.is_archived = workspace.is_archived
        await self.session.commit()

    async def delete(self, workspace_id : UUID) -> None:
        stmt = select(WorkspaceORM).where(WorkspaceORM.id == workspace_id)
        res = await self.session.execute(stmt)
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError("Workspace not found")
        orm.is_archived = True
        await self.session.commit()


    async def hard_delete(self, workspace_id : UUID) -> None:
        stmt = select(WorkspaceORM).where(WorkspaceORM.id == workspace_id)
        res = await self.session.execute(stmt)
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError("Workspace not found")
        await self.session.delete(orm)
        await self.session.commit()

    async def get(self, workspace_id : UUID) -> Workspace:
        stmt = select(WorkspaceORM).where(WorkspaceORM.id == workspace_id)
        res = await self.session.execute(stmt)
        orm = res.scalar_one_or_none()
        if orm is None:
            raise ValueError("Workspace not found")
        return Workspace(
            id=orm.id,
            name=orm.name,
            description=orm.description,
            is_archived=orm.is_archived,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    async def list_all(self) -> List[Workspace]:
        stmt = select(WorkspaceORM).where(WorkspaceORM.is_archived == False)
        res = await self.session.execute(stmt)
        rows = res.scalars().all()
        return [Workspace(
            id=obj.id,
            name=obj.name,
            description=obj.description,
            is_archived=obj.is_archived,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )
            for obj in rows
        ]

    async def exists(self, workspace_id : UUID) -> bool:
        stmt = select(WorkspaceORM.id).where(WorkspaceORM.id == workspace_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none() is not None







