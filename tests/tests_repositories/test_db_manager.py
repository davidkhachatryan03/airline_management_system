import os
from typing import Any
from uuid import UUID

import pytest
from uuid6 import uuid7

from src.common import DBManager
from src.common.exceptions import InvalidBytes
from src.entities import Passenger
from tests.factories import PassengerFactory


def test_db_manager_enter_and_exit(db: DBManager) -> None:
    with db:
        assert db.host == os.environ["DB_HOST"]
        assert db.user == os.environ["DB_USER"]
        assert db.password == os.environ["DB_TEST_PASS"]
        assert db.database == os.environ["DB_TEST_NAME"]

        assert db.connection.is_connected()

    assert not db.connection.is_connected()


def test_db_manager_connect_and_disconnect(db: DBManager) -> None:
    db.connect()

    assert db.connection.is_connected()

    db.disconnect()

    assert not db.connection.is_connected()


def test_db_manager_execute_sql_file(db_connected: DBManager) -> None:
    sql_file_route = "tests/fakes/fake_sql_file.sql"
    db_connected.execute_sql_file(sql_file_route)


def test_db_manager_retrieve(db_connected: DBManager) -> None:
    query = "SELECT 1"

    result: int = db_connected.retrieve_single_column(query)[0]

    assert result == 1


def test_db_manager_insert_rows(db_connected: DBManager) -> None:
    rows_count: int = db_connected.retrieve_single_column(
        "SELECT COUNT(*) FROM passengers"
    )[0]

    assert rows_count == 0

    passengers: list[Passenger] = PassengerFactory.build_batch(50)

    db_connected.insert_rows("passengers", passengers)

    rows_count: int = db_connected.retrieve_single_column(
        "SELECT COUNT(*) FROM passengers"
    )[0]

    assert rows_count == len(passengers)


def test_db_manager_uuid_to_bytes(db: DBManager) -> None:
    uuid_list: list[UUID] = [uuid7() for _ in range(10)]
    uuid_bytes_list: list[bytes] = db.uuid_to_bytes(uuid_list)

    for uuid in uuid_list:
        assert uuid.bytes in uuid_bytes_list


def test_db_manager_bytes_to_uuid_one_element_per_row(db: DBManager) -> None:
    uuid_bytes_list: list[bytes] = [uuid7().bytes for _ in range(10)]
    uuid_list: list[UUID] = db.bytes_to_uuid(uuid_bytes_list)

    for uuid in uuid_list:
        assert uuid.bytes in uuid_bytes_list


def test_db_manager_bytes_to_uuid_one_element_per_row_with_invalid_bytes(
    db: DBManager,
) -> None:
    invalid_uuid_bytes_list: list[tuple[Any, ...]] = [
        (uuid7(), b"1234567890123456", uuid7()) for _ in range(5)
    ]
    with pytest.raises(InvalidBytes):
        db.bytes_to_uuid(invalid_uuid_bytes_list)


def test_db_manager_bytes_to_uuid_many_elements_per_row(db: DBManager) -> None:
    random_rows_retrieved: list[tuple[Any, ...]] = [
        (uuid7().bytes, 1, "ABC", 12),
        (uuid7().bytes, 99, "CDE", 90),
    ]
    rows_processed: list[tuple] = db.bytes_to_uuid(random_rows_retrieved)

    for i in range(len(random_rows_retrieved)):
        for j in range(len(random_rows_retrieved[0])):
            if (
                isinstance(random_rows_retrieved[i][j], bytes)
                and len(random_rows_retrieved[i][j]) == 16
            ):
                assert rows_processed[i][j] == UUID(bytes=random_rows_retrieved[i][j])

            else:
                assert rows_processed[i][j] == random_rows_retrieved[i][j]


def test_db_manager_bytes_to_uuid_many_elements_per_row_with_invalid_bytes(
    db: DBManager,
) -> None:
    random_rows_retrieved_invalid_bytes: list[tuple[Any, ...]] = [
        (uuid7().bytes, 1, "ABC", 12),
        (uuid7().bytes, 99, "CDE", 90, b"1234567890123456"),
    ]
    with pytest.raises(InvalidBytes):
        db.bytes_to_uuid(random_rows_retrieved_invalid_bytes)
