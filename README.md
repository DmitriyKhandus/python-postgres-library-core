# python-postgres-library-core

Учебный проект по работе с PostgreSQL и FastAPI.

## Что реализовано

В проекте настроено API для работы с каталогом книг.

Реализованы:

- подключение к PostgreSQL;
- модели Category и Book через SQLAlchemy;
- Pydantic-схемы для входных и выходных данных;
- CRUD для категорий;
- CRUD для книг;
- фильтрация книг по категории;
- endpoint /health;
- Swagger-документация FastAPI;
- проверка данных в PostgreSQL.

## Структура проекта

app/
  api/
    categories.py
    books.py
  db/
    db.py
    models.py
    crud.py
  init_db.py
  main.py
  schemas.py

examples/
  result.jpg
  swagger-docs.jpg
  api-request.jpg

.gitignore
requirements.txt
README.md

## Локальные настройки

Для запуска проекта локально в корне проекта должен быть файл .env.

Пример содержимого файла .env:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=octagon_db
DB_USER=octagon
DB_PASSWORD=12345

Файл .env не загружается в GitHub, потому что он добавлен в .gitignore.

## Установка зависимостей

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Подготовка базы

python3 app/init_db.py

## Запуск API

uvicorn app.main:app --reload

После запуска доступны:

- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/categories/
- http://127.0.0.1:8000/books/

## Примеры проверки

Получить категории:

GET /categories/

Получить книги:

GET /books/

Отфильтровать книги по категории:

GET /books/?category_id=2

Создать категорию:

POST /categories/

Создать книгу:

POST /books/

## Скриншоты

Скриншоты результата работы API находятся в папке examples.
