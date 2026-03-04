from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer, Boolean, DateTime, func
from uuid import UUID
from .base import Base

class UserORM(Base):
    __tablename__ = 'users'

    id : Mapped[UUID] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String, nullable=False)
    second_name : Mapped[str] = mapped_column(String, nullable=False)
    email : Mapped[str] = mapped_column(String, nullable=False, unique=True)
    role : Mapped[str | None] = mapped_column(String, nullable=True)
    hashed_password : Mapped[str] = mapped_column(String, nullable=False)
    is_active : Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=func.now())
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),onupdate=func.now(), nullable=True)


