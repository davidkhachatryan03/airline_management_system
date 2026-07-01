import pytest

from src.common import DBManager

@pytest.fixture(scope="session", autouse=True)
def db_connected():
    db = DBManager()

    with db:
        yield db

@pytest.fixture(scope="function", autouse=True)
def revert_changes(db_connected: DBManager):
    db_connected.connection.start_transaction()

    yield db_connected

    db_connected.connection.rollback()