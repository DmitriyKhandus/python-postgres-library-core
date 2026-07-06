from fastapi import FastAPI

from app.api import books, categories
from app.db.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Books API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(categories.router)
app.include_router(books.router)
