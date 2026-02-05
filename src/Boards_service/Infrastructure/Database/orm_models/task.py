from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from uuid import UUID
from .base import Base
from .column import ColumnORM

class TaskORM(Base):
    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    column_id: Mapped[UUID] = mapped_column(ForeignKey("columns.id"))
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    #---relationship---
    column: Mapped["ColumnORM"] = relationship(back_populates="tasks")

