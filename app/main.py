import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.db.crud import read_books, read_categories
from app.db.db import SessionLocal


def show_catalog() -> None:
    with SessionLocal() as session:
        categories = read_categories(session)
        books = read_books(session)

    print("категории:")
    for category in categories:
        print(f"- {category.id}: {category.title}")

    print()
    print("книги:")

    for book in books:
        category_name = book.category.title if book.category else "без категории"

        print(f"- {book.title}")
        print(f"  категория: {category_name}")
        print(f"  цена: {book.price} руб.")
        print(f"  описание: {book.description}")
        print(f"  url: {book.url}")
        print()


if __name__ == "__main__":
    show_catalog()
