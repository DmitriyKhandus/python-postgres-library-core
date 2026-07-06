from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.dependencies import get_db
from app.db import crud

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=list[schemas.BookRead])
def read_books(
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_books(db, category_id=category_id)


@router.get("/{book_id}", response_model=schemas.BookRead)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book_by_id(db, book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@router.post(
    "/",
    response_model=schemas.BookRead,
    status_code=status.HTTP_201_CREATED
)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    category = crud.get_category_by_id(db, book.category_id)

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return crud.create_book(
        db,
        book.title,
        book.description,
        book.price,
        book.url,
        book.category_id
    )


@router.put("/{book_id}", response_model=schemas.BookRead)
def update_book(
    book_id: int,
    book_data: schemas.BookUpdate,
    db: Session = Depends(get_db)
):
    old_book = crud.get_book_by_id(db, book_id)

    if old_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    if book_data.category_id is not None:
        category = crud.get_category_by_id(db, book_data.category_id)

        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")

    updated_book = crud.update_book(
        db,
        book_id,
        title=book_data.title,
        description=book_data.description,
        price=book_data.price,
        url=book_data.url,
        category_id=book_data.category_id
    )

    return updated_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_book(db, book_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")

    return None
