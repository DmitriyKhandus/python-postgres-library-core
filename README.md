# python-postgres-library-core

Учебный проект по работе с PostgreSQL из Python.

## Что реализовано

В проекте настроена работа с базой данных PostgreSQL через SQLAlchemy.

Реализованы:

- подключение к базе данных;
- модели Category и Book;
- создание таблиц;
- CRUD-операции для категорий и книг;
- начальное заполнение базы;
- вывод данных из PostgreSQL в терминал.

## Структура проекта

app/
  db/
    db.py
    models.py
    crud.py
  init_db.py
  main.py

examples/
  result.jpg

.gitignore
requirements.txt
README.md

## Настройки подключения

Для запуска проекта локально в корне проекта должен быть файл .env.

Файл .env содержит параметры подключения к базе данных:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=octagon_db
DB_USER=octagon
DB_PASSWORD=12345

Файл .env не загружается в GitHub, потому что он находится в .gitignore.

## Установка зависимостей

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Запуск

Сначала нужно создать таблицы и заполнить базу:

python3 app/init_db.py

Затем можно вывести данные:

python3 app/main.py

## Скриншот

Скриншот результата работы программы находится в папке examples.
