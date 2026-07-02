import os
from uuid import UUID

from src.common import DBManager
from src.entities import Passenger

def test_db_manager_enter_and_exit(db: DBManager) -> None:
    with db:
        assert db.host == os.environ["DB_HOST"]
        assert db.user == os.environ["DB_USER"]
        assert db.password == os.environ["DB_PASS"]
        assert db.database == os.environ["DB_NAME"]

        assert db.connection.is_connected()

    assert not db.connection.is_connected()

def test_db_manager_connect_and_disconnect(db: DBManager) -> None:
    db.connect()

    assert db.connection.is_connected()

    db.disconnect()

    assert not db.connection.is_connected()

def test_db_manager_execute_sql_file(db_connected: DBManager, sql_file_route: str) -> None:
    db_connected.execute_sql_file(sql_file_route)

def test_db_manager_retrieve(db_connected: DBManager) -> None:
    query = "SELECT 1"

    result: int = db_connected.retrieve(query)[0]

    assert result == 1

def test_db_manager_insert_rows(db_connected: DBManager, passengers: list[Passenger]) -> None:
    rows_count: int = db_connected.retrieve("SELECT COUNT(*) FROM passengers")[0]

    assert rows_count == 0

    db_connected.insert_rows("passengers", passengers)

    rows_count: int = db_connected.retrieve("SELECT COUNT(*) FROM passengers")[0]

    assert rows_count == len(passengers)

def test_db_manager_uuid_to_bytes(db: DBManager, uuid_list: list[UUID]) -> None:
    uuid_bytes_list: list[bytes] = db.uuid_to_bytes(uuid_list)

    for uuid in uuid_list:
        assert uuid.bytes in uuid_bytes_list

def test_db_manager_bytes_to_uuid(db: DBManager, uuid_bytes_list: list[bytes]) -> None:
    uuid_list: list[UUID] = db.bytes_to_uuid(uuid_bytes_list)

    for uuid in uuid_list:
        assert uuid.bytes in uuid_bytes_list