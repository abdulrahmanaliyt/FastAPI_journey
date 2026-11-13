
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from .user import User
    from .enrollment import Enrollment


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    # One-to-one relationship with User
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=True
    )

    user: Mapped[User | None] = relationship(
        back_populates="student"
    )

    # One-to-many relationship with Enrollment
    enrollments: Mapped[list[Enrollment]] = relationship(
        back_populates="student",
        cascade="all, delete-orphan"
    )
