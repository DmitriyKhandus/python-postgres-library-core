from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.schemas import CategoryCreate, CategoryUpdate


router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    rows = db.execute(
        text("SELECT id, title FROM categories ORDER BY id")
    ).mappings().all()

    return [
        {
            "id": row["id"],
            "title": row["title"],
        }
        for row in rows
    ]


@router.get("/{category_id}")
def get_category(category_id: int, db: Session = Depends(get_db)):
    row = db.execute(
        text("SELECT id, title FROM categories WHERE id = :id"),
        {"id": category_id},
    ).mappings().first()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="категория не найдена",
        )

    return {
        "id": row["id"],
        "title": row["title"],
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
):
    try:
        row = db.execute(
            text("""
                INSERT INTO categories (title)
                VALUES (:title)
                RETURNING id, title
            """),
            {"title": category_data.title},
        ).mappings().first()

        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="категория с таким названием уже существует",
        )

    return {
        "id": row["id"],
        "title": row["title"],
    }


@router.put("/{category_id}")
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
):
    try:
        row = db.execute(
            text("""
                UPDATE categories
                SET title = :title
                WHERE id = :id
                RETURNING id, title
            """),
            {
                "id": category_id,
                "title": category_data.title,
            },
        ).mappings().first()

        if row is None:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="категория не найдена",
            )

        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="категория с таким названием уже существует",
        )

    return {
        "id": row["id"],
        "title": row["title"],
    }


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("DELETE FROM categories WHERE id = :id"),
        {"id": category_id},
    )

    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="категория не найдена",
        )

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
