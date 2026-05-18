import pytest
from src.common import DBManager

@pytest.fixture
def db_disconnected() -> DBManager:
    db = DBManager()
    db.connect()
    db.disconnect()
    return db

class TestEntity:
    
    def __init__(self, data: str) -> None:
        self.data = data

    def to_dict(self) -> dict:
        return {
            "data": self.data
        }
    
class InvalidTestEntity:

    def __init__(self, data: str) -> None:
        self.data = data

@pytest.fixture
def test_entity() -> TestEntity:
    test_entity = TestEntity("text")
    return test_entity

@pytest.fixture
def invalid_test_entity() -> InvalidTestEntity:
    invalid_test_entity = InvalidTestEntity("text")
    return invalid_test_entity