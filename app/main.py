from fastapi import FastAPI

from app.api import books, categories
from app.db.db import create_tables


app = FastAPI(
    title="library catalog api",
    description="API для работы с категориями и книгами через PostgreSQL.",
    version="1.0.0",
)


@app.on_event("startup")
def startup_event() -> None:
    create_tables()


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "database": "connected",
    }


app.include_router(categories.router)
app.include_router(books.router)
