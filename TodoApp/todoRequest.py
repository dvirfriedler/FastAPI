from pydantic import BaseModel, Field


class TodoRequest(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=3, max_length=50)
    priority: int = Field(gt=0, le=5)
    completed: bool