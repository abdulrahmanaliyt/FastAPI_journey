from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


class Course(Base):
  __tablename__ = "courses"

  id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
  title: Mapped[str] = mapped_column(String(100), nullable=False)
  duration: Mapped[int] = mapped_column(Integer, nullable=False)
  price: Mapped[float] = mapped_column(Float, nullable=False)