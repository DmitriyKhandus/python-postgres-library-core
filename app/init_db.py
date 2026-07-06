from app.db.db import Base, engine, SessionLocal
from app.db.crud import create_category, create_book

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

session = SessionLocal()

programming = create_category(session, "Программирование")
databases = create_category(session, "Базы данных")

create_book(
    session,
    "Python для начинающих",
    "Книга для изучения синтаксиса Python и базовых операторов.",
    1200.0,
    "",
    programming.id
)

create_book(
    session,
    "Автоматизация на Python",
    "Практическое пособие по автоматизации задач с помощью Python.",
    1550.0,
    "",
    programming.id
)

create_book(
    session,
    "Основы SQL",
    "Книга о базовых запросах SQL и работе с таблицами.",
    990.0,
    "",
    databases.id
)

create_book(
    session,
    "PostgreSQL на практике",
    "Практическое руководство по работе с PostgreSQL.",
    1800.0,
    "",
    databases.id
)

session.close()

print("База данных создана и заполнена категориями и книгами.")
