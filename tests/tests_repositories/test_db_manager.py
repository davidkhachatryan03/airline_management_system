import os

from src.common import DBManager


def test_db_manager_pool_is_shared() -> None:
    db1 = DBManager()
    db2 = DBManager()

    assert DBManager._pool is not None
    assert db1._pool is db2._pool


def test_db_manager_enter_and_exit(db: DBManager) -> None:
    with db:
        assert db.host == os.environ["DB_HOST"]
        assert db.user == os.environ["DB_USER"]
        assert db.password == os.environ["DB_TEST_PASS"]
        assert db.database == os.environ["DB_TEST_NAME"]

        assert db.connection.is_connected()

    assert getattr(db, "connection", None) is None


def test_db_manager_connect_and_disconnect(db: DBManager) -> None:
    db.connect()

    assert db.connection.is_connected()

    db.disconnect()

    assert getattr(db, "connection", None) is None


def test_db_manager_execute_sql_file(db_connected: DBManager) -> None:
    sql_file_route = "tests/fakes/fake_sql_file.sql"
    db_connected.execute_sql_file(sql_file_route)


def test_db_manager_execute_read(db_connected: DBManager) -> None:
    result: int = db_connected.execute_read(query="SELECT 1")[0][0]

    assert result == 1


def test_db_manager_execute_read_single_column(db_connected: DBManager) -> None:
    result: int = db_connected.execute_read_single_column(query="SELECT 1")[0]

    assert result == 1


def test_db_manager_execute_write(db_connected: DBManager) -> None:
    query = "INSERT INTO document_types VALUES (%s,%s)"
    values = (7, "document_type")

    result: int = db_connected.execute_write(query=query, values=values)

    query = "SELECT id, description FROM document_types WHERE id = 7"

    documen_type_retrieved = db_connected.execute_read(query=query)[0]

    assert result == 1
    assert documen_type_retrieved == values


def test_db_manager_execute_write_many(db_connected: DBManager) -> None:
    query = "INSERT INTO document_types VALUES (%s,%s)"
    values = [(7, "document_type_1"), (8, "document_type_2"), (9, "document_type_3")]

    result: int = db_connected.execute_write_many(query=query, values=values)

    query = "SELECT id, description FROM document_types WHERE id IN (7, 8, 9)"

    documen_type_retrieved = db_connected.execute_read(query=query)

    assert result == 3
    assert documen_type_retrieved == values
