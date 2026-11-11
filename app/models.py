from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Passenger(Base):
    __tablename__ = "passengers"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="passenger"
    )
    
class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)

    train_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    passenger_id: Mapped[int] = mapped_column(
        ForeignKey("passengers.id"),
        nullable=False
    )

    passenger: Mapped["Passenger"] = relationship(
        back_populates="bookings"
    )