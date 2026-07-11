from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from settings.database import Base


class Item(Base):
    __tablename__ = "items"

    item_id: Mapped[str] = mapped_column(String, primary_key=True)
    item_name: Mapped[str] = mapped_column(String, nullable=False)
    subcategory: Mapped[str] = mapped_column(String, nullable=False)


class Daily(Base):
    __tablename__ = "daily"
    __table_args__ = (
        Index("ix_daily_item_date", "item_id", "date"),
        Index("ix_daily_date", "date"),
    )

    date: Mapped["date"] = mapped_column(Date, primary_key=True)
    item_id: Mapped[str] = mapped_column(ForeignKey("items.item_id"), primary_key=True)

    fact: Mapped[float | None] = mapped_column(Float, nullable=True)
    sales: Mapped[float | None] = mapped_column(Float, nullable=True)
    math: Mapped[float] = mapped_column(Float, nullable=False)
    ml: Mapped[float] = mapped_column(Float, nullable=False)
    ruki: Mapped[float | None] = mapped_column(Float, nullable=True)
