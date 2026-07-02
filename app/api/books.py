from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.schemas import BookCreate, BookUpdate


router = APIRouter(
    prefix="/books",
    tags=["books"],
)


def get_book_dict(db: Session, book_id: int):
    query = text("""
        SELECT
            b.id,
            b.title,
            b.description,
            b.price,
            b.url,
            b.category_id,
            c.title AS category_title
        FROM books b
        LEFT JOIN categories c ON c.id = b.category_id
        WHERE b.id = :book_id
    """)

    row = db.execute(query, {"book_id": book_id}).mappings().first()

    if row is None:
        return None

    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "price": str(row["price"]),
        "url": row["url"],
        "category_id": row["category_id"],
        "category": {
            "id": row["category_id"],
            "title": row["category_title"],
        },
    }


@router.get("/")
def get_books(
    category_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    if category_id is not None:
        category = db.execute(
            text("SELECT id FROM categories WHERE id = :id"),
            {"id": category_id},
        ).first()

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="категория для фильтрации не найдена",
            )

        query = text("""
            SELECT
                b.id,
                b.title,
                b.description,
                b.price,
                b.url,
                b.category_id,
                c.title AS category_title
            FROM books b
            LEFT JOIN categories c ON c.id = b.category_id
            WHERE b.category_id = :category_id
            ORDER BY b.id
        """)

        rows = db.execute(query, {"category_id": category_id}).mappings().all()
    else:
        query = text("""
            SELECT
                b.id,
                b.title,
                b.description,
                b.price,
                b.url,
                b.category_id,
                c.title AS category_title
            FROM books b
            LEFT JOIN categories c ON c.id = b.category_id
            ORDER BY b.id
        """)

        rows = db.execute(query).mappings().all()

    return [
        {
            "id": row["id"],
            "title": row["title"],
            "description": row["description"],
            "price": str(row["price"]),
            "url": row["url"],
            "category_id": row["category_id"],
            "category": {
                "id": row["category_id"],
                "title": row["category_title"],
            },
        }
        for row in rows
    ]


@router.get("/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = get_book_dict(db, book_id)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="книга не найдена",
        )

    return book


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    category = db.execute(
        text("SELECT id FROM categories WHERE id = :id"),
        {"id": book_data.category_id},
    ).first()

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="нельзя создать книгу: категория не найдена",
        )

    query = text("""
        INSERT INTO books (title, description, price, url, category_id)
        VALUES (:title, :description, :price, :url, :category_id)
        RETURNING id
    """)

    created_id = db.execute(
        query,
        {
            "title": book_data.title,
            "description": book_data.description,
            "price": Decimal(book_data.price),
            "url": book_data.url,
            "category_id": book_data.category_id,
        },
    ).scalar_one()

    db.commit()

    return get_book_dict(db, created_id)


@router.put("/{book_id}")
def update_book(
    book_id: int,
    book_data: BookUpdate,
    db: Session = Depends(get_db),
):
    book = db.execute(
        text("SELECT id FROM books WHERE id = :id"),
        {"id": book_id},
    ).first()

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="книга не найдена",
        )

    category = db.execute(
        text("SELECT id FROM categories WHERE id = :id"),
        {"id": book_data.category_id},
    ).first()

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="нельзя обновить книгу: категория не найдена",
        )

    db.execute(
        text("""
            UPDATE books
            SET title = :title,
                description = :description,
                price = :price,
                url = :url,
                category_id = :category_id
            WHERE id = :book_id
        """),
        {
            "book_id": book_id,
            "title": book_data.title,
            "description": book_data.description,
            "price": Decimal(book_data.price),
            "url": book_data.url,
            "category_id": book_data.category_id,
        },
    )

    db.commit()

    return get_book_dict(db, book_id)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("DELETE FROM books WHERE id = :id"),
        {"id": book_id},
    )

    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="книга не найдена",
        )

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
