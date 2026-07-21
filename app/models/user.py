from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin
if TYPE_CHECKING:
    from app.models.role import Role
    from app.models.company import Company

class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true"),
    )
    
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False,
    )

    role: Mapped["Role"] = relationship(
        back_populates="users"
    )
    company_id: Mapped[int | None] = mapped_column(
        ForeignKey("companies.id"),
        nullable=True,
    )

    company: Mapped["Company"] = relationship(
        back_populates="users"
    )