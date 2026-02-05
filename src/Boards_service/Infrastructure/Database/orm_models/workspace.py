from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from uuid import UUID
from .base import Base
from .board import BoardORM

class WorkspaceORM(Base):
    __tablename__ = 'workspaces'

    id : Mapped[UUID] = mapped_column(primary_key=True)
    title : Mapped[str] = mapped_column(String, nullable=False)
    description : Mapped[str | None] = mapped_column(String, nullable=True)
    #---relationship---
    boards : Mapped[list['BoardORM']] = relationship (back_populates='workspace', cascade='all, delete-orphan')

