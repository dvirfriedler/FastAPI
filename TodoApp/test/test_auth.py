from .utils import *
from ..routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from jose import jwt
from datetime import timedelta
from fastapi import HTTPException



app.dependency_overrides[get_db] = override_get_db


def test_authenticated_user(test_user):
    db = TestingSessionLocal()
    
    authenticated_user = authenticate_user(test_user.username, 'admin', db)
    assert authenticated_user != False
    assert authenticated_user.username == test_user.username
    
    non_existentq_user = authenticate_user('non_existent', 'admin', db)
    assert non_existentq_user == False
    
    
    worng_password_user = authenticate_user(test_user.username, 'wrong_password', db)
    assert worng_password_user == False
    
def test_create_access_token():
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)
    
    token = create_access_token(username, user_id, role, expires_delta)
    decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False})
    
    assert decode_token.get('sub') == username
    assert decode_token.get('user_id') == user_id
    assert decode_token.get('role') == role
    
@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {"sub": 'testuser', "user_id": 1, 'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    
    user = await get_current_user(token)
    assert user == {'username': 'testuser', 'id': 1, 'user_role': 'admin'}
    

@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'role' : 'user'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token)
        
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate user authentication"

    
    
    
    
    
    
    
    
   