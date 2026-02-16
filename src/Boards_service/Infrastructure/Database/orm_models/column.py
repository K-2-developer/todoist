from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer, Boolean
from uuid import UUID
from .base import Base


class ColumnORM(Base):
    __tablename__ = 'columns'

    id : Mapped[UUID] = mapped_column(primary_key=True)
    board_id : Mapped[UUID] = mapped_column(ForeignKey('boards.id'))
    title : Mapped[str] = mapped_column(String, nullable=False)
    position : Mapped[int] = mapped_column(Integer, nullable=False)
    is_archived : Mapped[bool] = mapped_column(Boolean, nullable=False)
    #---relationship---
    board : Mapped['BoardORM'] = relationship(back_populates='columns')
    tasks : Mapped[list['TaskORM']] = relationship(back_populates='column', cascade='all, delete-orphan')


