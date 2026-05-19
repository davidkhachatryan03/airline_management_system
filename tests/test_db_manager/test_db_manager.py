import pytest, os
from src.common import DBManager
from src.common.exceptions import CursorNotFound, DatabaseError, SQLFileNotFound, NoConnection
from typing import cast

def test_connections() -> None:
    with DBManager() as db_test:
        db_test.connection.is_connected()
    
    assert db_test.connection.is_connected() == False

def test_execute_sql_file() -> None:
    with DBManager() as db_test:
        route = os.path.join(os.getcwd(), "tests/test_db_manager/utils/valid_sql_file_test.sql")

        db_test.execute_sql_file(route)

        row: tuple[int] = cast(tuple, db_test.cursor.fetchone())
        result: int = row[0]

    assert result == 1

@pytest.mark.parametrize("route, expected_exception", [
    ("", SQLFileNotFound),
    (os.getcwd(), DatabaseError),
    (os.path.join(os.getcwd(), "tests/test_db_manager/utils/invalid_sql_file_test.sql"), Exception)
])

def test_execute_sql_file_invalid_route(route: str, expected_exception) -> None:
    with DBManager() as db_test:

        with pytest.raises(expected_exception):
            db_test.execute_sql_file(route)
    
def test_execute_sql_file_no_connection(db_disconnected: DBManager) -> None:
    with pytest.raises(NoConnection):
        db_disconnected.execute_sql_file("")
    
def test_insert_row(test_entity) -> None:
    with DBManager() as db:
        db.execute_sql_file(os.path.join(os.getcwd(),"tests/test_db_manager/utils/create_db_test.sql"))
        db.choose_database("test")
        db.insert_row("test_table", test_entity)

        query = "SELECT * FROM test_table"

        result: tuple = cast(tuple, db.retrieve(query))
        expected_result = [(1, "text")]
    
    assert result == expected_result

def test_insert_invalid_row_no_to_dict_method(invalid_test_entity) -> None:
    with DBManager() as db:
        db.execute_sql_file(os.path.join(os.getcwd(),"tests/test_db_manager/utils/create_db_test.sql"))
        db.choose_database("test")

        with pytest.raises(ValueError):
            db.insert_row("test_table", invalid_test_entity)

def test_insert_invalid_row_SQL_exception(test_entity) -> None:
    with DBManager() as db:
        db.execute_sql_file(os.path.join(os.getcwd(),"tests/test_db_manager/utils/create_db_test.sql"))
        db.choose_database("test")

        with pytest.raises(DatabaseError):
            db.insert_row("", test_entity)
    
def test_choose_database() -> None:
    with DBManager() as db:
        db.execute_sql_file(os.path.join(os.getcwd(),"tests/test_db_manager/utils/create_db_test.sql"))
        db.choose_database("test")

        query = "SELECT DATABASE()"

        result: str = cast(str, db.retrieve(query)[0])
        expected_result: str = "test"

    assert result == expected_result

def test_choose_invalid_database() -> None:
    with DBManager() as db:
    
        with pytest.raises(DatabaseError):
            db.choose_database("inexistent database.")

@pytest.mark.parametrize("query, values, expected_result", [
    ("SELECT 1;", (), [1]),
    ("SELECT %s;", (1,), [1]),
    ("SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3;", (), [1,2,3]),
    ("SELECT 1, 'a' UNION ALL SELECT 2, 'b' UNION ALL SELECT 3, 'c';", (), [(1,"a"),(2,"b"),(3,"c")])
])

def test_retrieve(query: str, values: tuple | list, expected_result) -> None:
    with DBManager() as db:
        result = db.retrieve(query, values)

    assert result == expected_result

def test_retrieve_no_connection(db_disconnected: DBManager) -> None:
    with pytest.raises(NoConnection):
        db_disconnected.retrieve("SELECT 1;")