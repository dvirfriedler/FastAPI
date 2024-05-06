from fastapi import Depends, HTTPException, Path, Query, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
import models
from models import Todos,Users
from database import engine , SessionLocal
from starlette import status
from todoRequest import TodoRequest
from .auth import get_current_user, bcyrpt_context




router = APIRouter(prefix="/admin"
                   , tags=["admin"])
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
    
        
@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency,
                   db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Todos).all()

@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT) 
async def delete_user(user: user_dependency,
                    db: db_dependency,
                      user_id: int):
    user = db.query(user).filter(user.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency,
                      db: db_dependency, 
                      todo_id: int = Path(gt=0)):
    
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model:
        db.delete(todo_model)
        db.commit()
        return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")

@router.put("/reset_password/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(user: user_dependency,
                         db: db_dependency,
                         user_id: int):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = bcyrpt_context.hash("00000")
    db.commit()
    return {"message": "Password reset successfully"}   





