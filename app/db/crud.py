from decimal import Decimal

from sqlalchemy import delete, select
from sqlalchemy.orm import Session, selectinload

from app.db.models import Book, Category


def reset_catalog(session: Session) -> None:
    session.execute(delete(Book))
    session.execute(delete(Category))
    session.commit()


def create_category(session: Session, title: str) -> Category:
    category = session.scalar(
        select(Category).where(Category.title == title)
    )

    if category is not None:
        return category

    category = Category(title=title)
    session.add(category)
    session.commit()
    session.refresh(category)

    return category


def read_categories(session: Session) -> list[Category]:
    query = select(Category).order_by(Category.id)
    return list(session.scalars(query))


def rename_category(
    session: Session,
    current_title: str,
    new_title: str,
) -> Category | None:
    category = session.scalar(
        select(Category).where(Category.title == current_title)
    )

    if category is None:
        return None

    category.title = new_title
    session.commit()
    session.refresh(category)

    return category


def delete_category(session: Session, title: str) -> bool:
    category = session.scalar(
        select(Category).where(Category.title == title)
    )

    if category is None:
        return False

    session.delete(category)
    session.commit()

    return True


def create_book(
    session: Session,
    title: str,
    description: str,
    price: Decimal,
    url: str,
    category_id: int,
) -> Book:
    book = Book(
        title=title,
        description=description,
        price=price,
        url=url,
        category_id=category_id,
    )

    session.add(book)
    session.commit()
    session.refresh(book)

    return book


def read_books(session: Session) -> list[Book]:
    query = (
        select(Book)
        .options(selectinload(Book.category))
        .order_by(Book.id)
    )

    return list(session.scalars(query))


def change_book_price(
    session: Session,
    title: str,
    new_price: Decimal,
) -> Book | None:
    book = session.scalar(
        select(Book).where(Book.title == title)
    )

    if book is None:
        return None

    book.price = new_price
    session.commit()
    session.refresh(book)

    return book


def delete_book(session: Session, title: str) -> bool:
    book = session.scalar(
        select(Book).where(Book.title == title)
    )

    if book is None:
        return False

    session.delete(book)
    session.commit()

    return True
