from fastapi import Depends, HTTPException, Path, Query, APIRouter
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import models
from models import Todos,Users
from database import engine , SessionLocal
from starlette import status
from todoRequest import TodoRequest
from .auth import get_current_user, bcyrpt_context




router = APIRouter(prefix="/user"
                   , tags=["user"])

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class UserVerification(BaseModel):
    current_password: str
    new_password: str = Field(min_length=5)

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user_info(user: user_dependency, 
                        db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_info = db.query(Users).filter(Users.id == user.get('id')).first()
    return user_info


@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency,
                          db: db_dependency,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcyrpt_context.verify(user_verification.current_password, user_model.hashed_password):
        raise HTTPException(status_code=400, detail="Passwords do not match")
    user_model.hashed_password = bcyrpt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
    return {"message": "Password updated successfully"}

@router.put('/phonenumber/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency,
                              db: db_dependency,
                              phone_number: str = Path(min_length=10, max_length=10)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
    return {"message": "Phone number updated successfully"}

