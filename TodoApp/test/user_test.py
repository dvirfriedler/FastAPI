from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status
from ..routers.auth import bcyrpt_context

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = overrid_get_current_user

def test_return_user(test_user):
    respnse = client.get("/user")
    assert respnse.status_code == status.HTTP_200_OK
    assert respnse.json()['username'] == 'dvirfriedler'
    assert respnse.json()['email'] == 'dvir@.com'
    assert respnse.json()['first_name'] == 'dvir'
    assert respnse.json()['last_name'] == 'friedler'
    assert respnse.json()['role'] == 'admin'
    assert respnse.json()['phone_number'] == '0523154561'
    
def test_change_password_success(test_user):
    request_data = {
        'current_password': 'admin',
        'new_password': '12345'
    }
    
    response = client.put("/user/password", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_wrong_pass(test_user):
    request_data = {
        'current_password': 'WROGN_PASSWORD',
        'new_password': '12345'
    }
    
    response = client.put("/user/password", json=request_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Passwords do not match"}
    
def test_change_phone_number_success(test_user):
        response = client.put("/user/phonenumber/0525555555")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        

    

    
    