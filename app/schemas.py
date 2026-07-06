from typing import Optional
from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    title: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    title: str


class CategoryRead(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: str
    description: str
    price: float
    url: str = ""
    category_id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    url: Optional[str] = None
    category_id: Optional[int] = None


class BookRead(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
