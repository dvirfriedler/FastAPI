from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel
from book import Book
from book_request import BookRequest
from starlette import status

app = FastAPI()

BOOKS =[
    Book(1, 'Title One', 'Author One', 'Description One', 5, 2021),
    Book(2, 'Title Two', 'Author Two', 'Description Two', 4, 2020),
    Book(3, 'Title Three', 'Author Three', 'Description Three', 3, 2019),
    Book(4, 'Title Four', 'Author Four', 'Description Four', 2 , 2018),
    Book(5, 'Title Five', 'Author Five', 'Description Five', 1, 2020),
    Book(6, 'Title Six', 'Author Six', 'Description Six', 0, 2018),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
        raise HTTPException(status_code=404, detail="Book not found")
        
        
@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_books_by_rating(rating: int = Query(ge=0, le=5 )):
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/books/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = len(BOOKS) + 1
    return book

@app.put("/books/update-book/", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_change = True

    if not book_change:
        raise HTTPException(status_code=404, detail="Book not found")
        
        
@app.delete("/books/{book_id}",  status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int =  Path(gt=0)) :
    book_deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_deleted = True
    if not book_deleted:
        raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/by_date/", status_code=status.HTTP_200_OK)
async def get_books_by_date(published_date: int = Query(ge=1949, le=2100)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return





