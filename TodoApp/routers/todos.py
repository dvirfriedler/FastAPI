from fastapi import Depends, HTTPException, Path, Query, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
import models
from models import Todos
from database import engine , SessionLocal
from starlette import status
from todoRequest import TodoRequest



router = APIRouter()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
    
        
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()

@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db : db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.dict())
    db.add(todo_model)
    db.commit()
    return todo_model

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, 
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model:
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.completed = todo_request.completed
        todo_model.priority = todo_request.priority
        
        db.add(todo_model)
        db.commit()
        return
    raise HTTPException(status_code=404, detail="Todo not found")

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model:
        db.delete(todo_model)
        db.commit()
        return
    raise HTTPException(status_code=404, detail="Todo not found")


