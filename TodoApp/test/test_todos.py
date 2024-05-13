from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..main import app
from ..routers.todos import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from ..models import Todos


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
 
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = overrid_get_current_user

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

def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{ "completed": False, "title" : "Test Todo", "description": "Test Description", "priority": 5, 'id' : 1,"owner_id": 1}]


def test_read_one_authenticated(test_todo):
    response = client.get("/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == { "completed": False, "title" : "Test Todo", "description": "Test Description", "priority": 5, 'id' : 1,"owner_id": 1}



def test_read_one_not_found():
    response = client.get("/todos/2")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}
    
    
def test_create_todo(test_todo):
    request_data = {
        'title': 'Test Todo',
        'description': 'Test Description',
        'priority': 5,
        'completed': False
    }
    
    respone = client.post('todo/', json=request_data)
    assert respone.status_code == 201
    db = TestingSessionLocal()
    todo = db.query(Todos).filter(Todos.id == 2).first()
    assert todo.title == request_data.get('title')
    assert todo.description == request_data.get('description')
    assert todo.priority == request_data.get('priority')
    assert todo.completed == request_data.get('completed')
    
def test_update_todo(test_todo):
    request_data = {
        'title': 'Updated Todo',
        'description': 'Updated Description',
        'priority': 1,
        'completed': False
    }
    
    response = client.put('/todo/1', json=request_data)
    assert response.status_code == 204
    db = TestingSessionLocal()
    todo = db.query(Todos).filter(Todos.id == 1).first()
    assert todo.title == request_data.get('title')
    assert todo.description == request_data.get('description')
    assert todo.priority == request_data.get('priority')
    assert todo.completed == request_data.get('completed')
    
    
def test_update_not_found(test_todo):
    request_data = {
        'title': 'Updated Todo',
        'description': 'Updated Description',
        'priority': 1,
        'completed': False
    }
    
    response = client.put('/todo/999', json=request_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
    
def test_delete_todo(test_todo):
    response = client.delete('/todo/1')
    assert response.status_code == 204
    db = TestingSessionLocal()
    todo = db.query(Todos).filter(Todos.id == 1).first()
    assert todo is None
    
def test_delete_todo_not_found(test_todo):
    response = client.delete('/todo/999')
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
    
    