from datetime import timedelta, datetime
from typing import Annotated
from fastapi import Depends, FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from starlette import status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

router = APIRouter(prefix="/auth"
                   , tags=["auth"])

bcyrpt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


SECRET_KEY = "28d1badfbd41ac87a524badff22f2b438c1e5337a97888466900e5539657c481"
ALGORITHM = "HS256"




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcyrpt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str,user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "user_id": user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user authentication")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user authentication")
    return {'username': username, 'user_id': user_id}




class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, 
                      create_user_request: CreateUserRequest):
    try:
        create_user_model = Users(
            email = create_user_request.email,
            username = create_user_request.username,
            full_name = create_user_request.first_name,
            last_name = create_user_request.last_name,
            role = create_user_request.role,
            hashed_password = bcyrpt_context.hash(create_user_request.password),
            is_active = True
            )
        
        db.add(create_user_model)
        db.commit()
        return create_user_model
    
    except Exception as e:
        return str(e)
        
        
    
@router.post("/token", response_model=Token)
async def login(from_data: Annotated [OAuth2PasswordRequestForm , Depends()],
                db : db_dependency):
    
    user = authenticate_user(from_data.username, from_data.password, db)
    if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user authentication")
    token = create_access_token(username=from_data.username, user_id=user.id, expires_delta=timedelta(minutes=15))
    return {"access_token": token, "token_type": "bearer"}


@router.get("/users/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Users).all()
    
