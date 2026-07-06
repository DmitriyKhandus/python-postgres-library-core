from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False, unique=True)

    books = relationship("Book", back_populates="category", cascade="all, delete")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    url = Column(String(300), default="")
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="books")
