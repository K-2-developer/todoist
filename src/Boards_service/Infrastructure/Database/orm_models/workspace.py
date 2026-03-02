from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime, func
from datetime import datetime
from uuid import UUID
from .base import Base


class WorkspaceORM(Base):
    __tablename__ = 'workspaces'

    id : Mapped[UUID] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String, nullable=False)
    description : Mapped[str | None] = mapped_column(String, nullable=True)
    is_archived : Mapped[bool] = mapped_column(Boolean, nullable=False,default=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=func.now())
    updated_at : Mapped[datetime | None] = mapped_column(DateTime(timezone=True),onupdate=func.now(),nullable=True)
    #user_id
    #---relationship---
    boards : Mapped[list['BoardORM']] = relationship (back_populates='workspace', cascade='all, delete-orphan')

