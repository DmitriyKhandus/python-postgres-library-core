from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    books: Mapped[list["Book"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan",
    )


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    url: Mapped[str] = mapped_column(String(255), default="", nullable=False)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False,
    )

    category: Mapped[Category] = relationship(back_populates="books")
