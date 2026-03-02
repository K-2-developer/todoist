from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer, Boolean, DateTime, func
from uuid import UUID
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id : Mapped[UUID] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String, nullable=False)
    second_name : Mapped[str] = mapped_column(String, nullable=False)
    email : Mapped[str] = mapped_column(String, nullable=False, unique=True)
    role : Mapped[str] = mapped_column(String, nullable=False)
    password : Mapped[str] = mapped_column(String, nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=func.now())
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),unupdate=func.now())


