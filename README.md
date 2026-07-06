# books api

Учебный проект на Python с использованием FastAPI, PostgreSQL и SQLAlchemy.

Проект реализует API для работы с книгами и категориями книг.  
Данные хранятся в базе данных PostgreSQL.

## что реализовано

- подключение к PostgreSQL через SQLAlchemy;
- модели `Book` и `Category`;
- CRUD-операции для книг и категорий;
- роутеры FastAPI для `books` и `categories`;
- фильтрация книг по категории;
- endpoint `/health` для проверки работы приложения;
- автоматическая документация FastAPI через `/docs`;
- скриншоты результата работы в папке `examples/`.

## структура проекта

```text
app/
├── api/
│   ├── books.py
│   └── categories.py
├── db/
│   ├── crud.py
│   ├── db.py
│   └── models.py
├── dependencies.py
├── init_db.py
├── main.py
└── schemas.py

examples/
requirements.txt
.gitignore
README.md
```

## подготовка базы данных

Проект использует PostgreSQL в WSL.

Нужно создать пользователя PostgreSQL:

```bash
sudo -u postgres psql
```

Внутри PostgreSQL выполнить:

```sql
CREATE USER octagon WITH PASSWORD '12345';
CREATE DATABASE octagon_db OWNER octagon;
GRANT ALL PRIVILEGES ON DATABASE octagon_db TO octagon;
```

Выйти из PostgreSQL:

```sql
\q
```

## переменные окружения

Для запуска проекта локально нужно создать файл `.env` в корне проекта.

Пример содержимого:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=octagon_db
DB_USER=octagon
DB_PASSWORD=12345
```

Файл `.env` не загружается в GitHub, потому что содержит параметры подключения к базе данных.  
Он добавлен в `.gitignore`.

## установка зависимостей

Создать виртуальное окружение:

```bash
python3 -m venv venv
```

Активировать виртуальное окружение:

```bash
source venv/bin/activate
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

## заполнение базы данных

Перед запуском API нужно создать таблицы и заполнить базу начальными данными:

```bash
python3 -m app.init_db
```

После выполнения команды в базе появятся категории и книги.

## запуск проекта

Запустить сервер FastAPI:

```bash
uvicorn app.main:app --reload
```

После запуска приложение будет доступно по адресу:

```text
http://127.0.0.1:8000
```

## проверка работы

Проверка состояния приложения:

```text
http://127.0.0.1:8000/health
```

Документация Swagger:

```text
http://127.0.0.1:8000/docs
```

В документации можно проверить endpoints:

```text
GET /categories/
POST /categories/
GET /categories/{category_id}
PUT /categories/{category_id}
DELETE /categories/{category_id}

GET /books/
GET /books/?category_id=1
POST /books/
GET /books/{book_id}
PUT /books/{book_id}
DELETE /books/{book_id}
```

## результат

Проект запускает FastAPI-сервер, подключается к PostgreSQL и позволяет работать с книгами и категориями через API.

Скриншоты результата работы находятся в папке `examples/`.
