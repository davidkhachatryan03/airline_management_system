import pytest, os
from src.common import DBManager
from src.common.exceptions import CursorNotFound, DatabaseError, SQLFileNotFound, NoConnection
from typing import cast

def test_connections(db_test: DBManager) -> None:
    with pytest.raises(AttributeError):
        db_test.connection

    with pytest.raises(AttributeError):
        db_test.cursor

    db_test.connect()

    assert db_test.connection.is_connected() == True

    db_test.disconnect()

    assert db_test.connection.is_connected() == False

def test_execute_sql_file(db_test: DBManager) -> None:
    db_test.connect()
    route = os.path.join(os.getcwd(), "tests/test_db_manager/valid_sql_file_test.sql")

    db_test.execute_sql_file(route)

    row: tuple[int] = cast(tuple, db_test.cursor.fetchone())
    result: int = row[0]

    assert result == 1

@pytest.mark.parametrize("route, expected_exception", [
    ("", SQLFileNotFound),
    (os.getcwd(), DatabaseError),
    (os.path.join(os.getcwd(), "tests/test_db_manager/invalid_sql_file_test.sql"), Exception)
])

def test_execute_sql_file_invalid_route(db_test: DBManager, route: str, expected_exception) -> None:
    db_test.connect()

    with pytest.raises(expected_exception):
        db_test.execute_sql_file(route)

def test_execute_sql_file_no_connection(db_test: DBManager) -> None:
    db_test.connect()

    db_test.disconnect()

    with pytest.raises(NoConnection):
        db_test.execute_sql_file("")

def test_insert_row(db_test: DBManager, test_entity) -> None:
    db_test.connect()

    db_test.execute_sql_file(os.path.join(os.getcwd(),"tests/test_db_manager/create_db_test.sql"))
    db_test.choose_database("test")
    db_test.insert_row("test_table", test_entity)

    query = "SELECT * FROM test_table"

    result: tuple = cast(tuple, db_test.retrieve(query))
    expected_result = (1, "text")

    assert result == expected_result