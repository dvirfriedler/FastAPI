from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from starlette import status
from passlib.context import CryptContext

from models import Users

router = APIRouter()

bcyrpt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    

@router.post("/auth/",status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest):
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        full_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        hashed_password = bcyrpt_context.hash(create_user_request.password),
        is_active = True
        )
    
    return create_user_model
