
from ..routers.todos import get_db, get_current_user
from fastapi import status
from ..models import Todos
from .utils import *

 
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = overrid_get_current_user



def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{ "completed": False, "title" : "Test Todo", "description": "Test Description", "priority": 5, 'id' : 1,"owner_id": 1}]


def test_read_one_authenticated(test_todo):
    response = client.get("/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == { "completed": False, "title" : "Test Todo", "description": "Test Description", "priority": 5, 'id' : 1,"owner_id": 1}



def test_read_one_not_found():
    response = client.get("/todos/999")
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
    
    