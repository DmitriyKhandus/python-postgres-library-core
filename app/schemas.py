from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    title: str = Field(min_length=2, max_length=120)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class BookBase(BaseModel):
    title: str = Field(min_length=2, max_length=180)
    description: str = Field(min_length=5)
    price: Decimal = Field(gt=0)
    url: str = ""
    category_id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookRead(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category: CategoryRead | None = None
