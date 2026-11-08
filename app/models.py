from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

# A SQLAlchemy model describes a database table. It does not automatically create that table until we call Base.metadata.create_all().

class Student(Base):
    __tablename__ = "students"  #__tablename__	PostgreSQL table name

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    course: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )