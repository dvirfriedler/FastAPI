from fastapi import FastAPI
from book import Book

app = FastAPI()

BOOKS =[
    Book(1, 'Title One', 'Author One', 'Description One', 5),
    Book(2, 'Title Two', 'Author Two', 'Description Two', 4),
    Book(3, 'Title Three', 'Author Three', 'Description Three', 3),
    Book(4, 'Title Four', 'Author Four', 'Description Four', 2),
    Book(5, 'Title Five', 'Author Five', 'Description Five', 1),
    Book(6, 'Title Six', 'Author Six', 'Description Six', 0),
]





@app.get("/books")
async def read_all_books():
    return BOOKS

