import datetime
from decimal import Decimal

from sqlalchemy import Text, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class EventDB(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(Text)
    date: Mapped[datetime.date] = mapped_column()
    location: Mapped[str] = mapped_column(Text)

    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[Decimal | None] = mapped_column(Numeric)