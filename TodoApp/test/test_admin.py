from .utils import *
from ..routers.admin import get_db, get_current_user
from fastapi import status
from ..models import Todos




app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = overrid_get_current_user



def test_admin_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == [{ "completed": False, "title" : "Test Todo", "description": "Test Description", "priority": 5, 'id' : 1,"owner_id": 1}]
    
def test_admin_delete_todos(test_todo):
    response = client.delete("/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    todo = db.query(Todos).filter(Todos.id == 1).first()
    assert todo is None
    
def test_admin_delete_todo_not_found(test_todo):
    response = client.delete("/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}
    
def test_resert_password(test_user):
    response = client.put("/reset_password/1")
    #assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    user = db.query(Users).filter(Users.id == 1).first()
    assert user.hashed_password != bcyrpt_context.hash("00000")
    
    

    
    

    


    
    