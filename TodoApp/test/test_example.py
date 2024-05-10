import pytest


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, yaers : int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = yaers
  
@pytest.fixture
def default_student():
    return Student("John", "Doe", "Computer Science", 4)      
        
def test_person_initialization(default_student):
    assert default_student.first_name == "John"
    assert default_student.last_name == "Doe"
    assert default_student.major == "Computer Science"
    assert default_student.years == 4
    


def test_equal_or_not_equal():
    assert 1 == 1
    
def test_is_instane():
    assert isinstance(1, int)
    assert not isinstance(1, str)
    
    
def test_is_not_none():
    assert "hello" is not None
    assert None is None
    
def test_type():
    assert type(1) == int
    assert type(1.0) == float
    assert type("hello") == str
    
    
    

