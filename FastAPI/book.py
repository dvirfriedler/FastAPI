class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    
    
    def __init__(self, id: int, title: str, author: str, description: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating