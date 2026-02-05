from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from uuid import UUID
from .base import Base
from .workspace import WorkspaceORM
from .column import ColumnORM


class BoardORM(Base):
    __tablename__ = 'boards'

    id : Mapped[UUID] = mapped_column(primary_key=True)
    workspace_id : Mapped[UUID] = mapped_column(ForeignKey('workspaces.id'))
    title : Mapped[str] = mapped_column(String, nullable=False)
    description : Mapped[str | None] = mapped_column(String, nullable=True)
    #---relationship___
    workspace : Mapped['WorkspaceORM'] = relationship(back_populates='boards')
    columns : Mapped[list['ColumnORM']] = relationship(back_populates='board', cascade='all, delete-orphan')


