from typing import Optional
from pydantic import BaseModel, Field


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3, max_length=50)
    author: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=3, max_length=50)
    rating: int = Field(ge=-1, le=50)
    published_date: int = Field(ge= 1949, le=2100)