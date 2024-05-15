from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..database import Base
import pytest
from fastapi.testclient import TestClient
from ..main import app
from ..models import Todos, Users
from ..routers.auth import bcyrpt_context




SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"



engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False},
                       poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def overrid_get_current_user():
    return{"id": 1, "username": "testuser", 'user_role': 'admin'}      

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(title="Test Todo",
                 description="Test Description",
                 priority=5,
                 completed=False,
                 owner_id=1)
    
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()
        
@pytest.fixture
def test_user():
    user = Users(
        username="dvirfriedler",
        email="dvir@.com",
        first_name="dvir",
        last_name="friedler",
        hashed_password=bcyrpt_context.hash("admin"),
        role="admin",
        phone_number="0523154561"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()