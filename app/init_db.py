import sys
from decimal import Decimal
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.db.crud import (
    change_book_price,
    create_book,
    create_category,
    delete_book,
    read_books,
    read_categories,
    rename_category,
    reset_catalog,
)
from app.db.db import SessionLocal, create_tables


def prepare_database() -> None:
    create_tables()

    with SessionLocal() as session:
        reset_catalog(session)

        backend = create_category(session, "backend-разработка")
        databases = create_category(session, "базы данных")
        practice = create_category(session, "практика программирования")
        temporary = create_category(session, "временный раздел")

        rename_category(
            session,
            current_title="временный раздел",
            new_title="черновой раздел",
        )

        create_book(
            session,
            title="python для рабочего проекта",
            description="Практическая книга о структуре Python-приложения.",
            price=Decimal("790.00"),
            url="https://example.com/python-project",
            category_id=backend.id,
        )

        create_book(
            session,
            title="postgresql без лишней магии",
            description="Короткое введение в таблицы, связи и SQL-запросы.",
            price=Decimal("920.50"),
            url="https://example.com/postgres-simple",
            category_id=databases.id,
        )

        create_book(
            session,
            title="sqlalchemy в небольших приложениях",
            description="Материал про модели, сессии и CRUD-операции.",
            price=Decimal("1050.00"),
            url="https://example.com/sqlalchemy-apps",
            category_id=databases.id,
        )

        create_book(
            session,
            title="чистая структура учебного проекта",
            description="Книга о том, как не превращать папки проекта в хаос.",
            price=Decimal("610.00"),
            url="https://example.com/project-structure",
            category_id=practice.id,
        )

        create_book(
            session,
            title="запись для проверки удаления",
            description="Эта книга нужна только для демонстрации delete.",
            price=Decimal("100.00"),
            url="https://example.com/remove",
            category_id=temporary.id,
        )

        change_book_price(
            session,
            title="postgresql без лишней магии",
            new_price=Decimal("970.00"),
        )

        delete_book(session, "запись для проверки удаления")

        categories_count = len(read_categories(session))
        books_count = len(read_books(session))

    print("инициализация базы выполнена")
    print(f"категорий в базе: {categories_count}")
    print(f"книг в базе: {books_count}")


if __name__ == "__main__":
    prepare_database()
