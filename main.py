# To start the program run: uvicorn main:app --reload

from fastapi import FastAPI

app = FastAPI()

items = ['Item 0', 'Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6', 'Item 7', 'Item 8', 'Item 9']


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": {items[item_id]}, "q": q}

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return items[skip: skip + limit]


