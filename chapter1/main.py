import json
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.responses import JSONResponse
from pydantic import BaseModel

from models import Book
import router_example

app = FastAPI()

app.include_router(router_example.router)


class BookResponse(BaseModel):
    title: str
    author: str


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": "Oops! Something went wrong",
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return PlainTextResponse(
        "This is a Plain text response:" f" \n{json.dumps(exc.errors(),indent=2)}",
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@app.get("/error_endpoint")
async def raise_error():
    raise HTTPException(status_code=400)


@app.get("/allbooks")
async def read_all_books() -> list[BookResponse]:
    return [
        {
            "id": 1,
            "title": "1984",
            "author": "George Orwell",
        },
        {
            "id": 1,
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
        },
    ]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    return {
        "book_id": book_id,
        "title": "The Great Gastby",
        "author": "F. Scott Fitzgerald",
    }


@app.get("/books")
async def read_books(year: int = None):
    if year:
        return {"year": year, "books": ["Book 1", "Book 2"]}
    return {"books": "All books"}


@app.get("/authors/{author_id}")
async def read_author(author_id: int):
    return {
        "author_id": author_id,
        "name": "F. Scott Fitzgerald",
    }


@app.post("/book")
async def create_book(book: Book):
    return book
