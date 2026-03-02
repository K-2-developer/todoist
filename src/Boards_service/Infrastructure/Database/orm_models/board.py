from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer, Boolean, DateTime, func
from uuid import UUID
from .base import Base



class BoardORM(Base):
    __tablename__ = 'boards'

    id : Mapped[UUID] = mapped_column(primary_key=True)
    workspace_id : Mapped[UUID] = mapped_column(ForeignKey('workspaces.id'))
    title : Mapped[str] = mapped_column(String, nullable=False)
    description : Mapped[str | None] = mapped_column(String, nullable=True)
    position : Mapped[int] = mapped_column(Integer,nullable=False,default=0)
    is_archived : Mapped[bool] = mapped_column(Boolean,nullable=False,default=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,server_default=func.now())
    updated_at : Mapped[datetime | None] = mapped_column(DateTime(timezone=True),onupdate=func.now(), nullable=True)
    #---relationship___
    workspace : Mapped['WorkspaceORM'] = relationship(back_populates='boards')
    columns : Mapped[list['ColumnORM']] = relationship(back_populates='board', cascade='all, delete-orphan')


