from fastapi import Body,FastAPI

# To run the server, run the following command in the terminal: uvicorn books:app --reload

app = FastAPI()

BOOKS = [   {'title' : 'Title One', 'author' : 'Author One', 'category': 'science'},
            {'title' : 'Title Two', 'author' : 'Author Two', 'category': 'science'},
            {'title' : 'Title Three', 'author' : 'Author Three', 'category': 'History'},
            {'title' : 'Title Four', 'author' : 'Author Four', 'category': 'maths'},
            {'title' : 'Title Five', 'author' : 'Author Five', 'category': 'maths'},
            {'title' : 'Title Six', 'author' : 'Author Two', 'category': 'maths'},

]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_title}")
async def read_all_books(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
        
@app.get("/books/{author}/")
async def read_author_category_by_query(book_author: str ,category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
            book.get('category').casefold() == category.casefold():
             books_to_return.append(book)
    
    return books_to_return

@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    
    
@app.post("/books/update_book/{book_title}")
async def update_book(book_title: str, updated_book=Body()):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            book.update(updated_book)
            return book
        
        
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            

@app.get("/books/byauthor/{author}")
async def get_books_by_author(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return

    
        



