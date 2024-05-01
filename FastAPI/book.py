class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int
    
    
    def __init__(self, id: int, title: str, author: str, description: str, rating: int, published_date: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date