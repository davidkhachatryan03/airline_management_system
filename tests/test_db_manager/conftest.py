import pytest
from src.common import DBManager

@pytest.fixture(scope="session")
def db_test() -> DBManager:
    db_manager = DBManager()
    return db_manager

def db_connected_test(db_manager : DBManager) ->


class TestEntity:
        def __init__(self, data: str) -> None:
            self.data = data

        def to_dict(self) -> dict:
            return {
                "data": self.data
            }

@pytest.fixture
def test_entity() -> TestEntity:
    test_entity = TestEntity("text")
    return test_entity