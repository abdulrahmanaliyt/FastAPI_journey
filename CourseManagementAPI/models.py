from decimal import Decimal

from sqlalchemy import Float, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


class Course(Base):
  __tablename__ = "courses"

  id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
  title: Mapped[str] = mapped_column(String(100), nullable=False)
  duration: Mapped[int] = mapped_column(Integer, nullable=False)
  price: Mapped[Decimal] = mapped_column(
    Numeric(10, 2),
    nullable=False
)