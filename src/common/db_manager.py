import os
from typing import Any, Sequence, cast

from dotenv import load_dotenv
from mysql.connector import pooling
from mysql.connector.cursor import MySQLCursor
from mysql.connector.pooling import PooledMySQLConnection

load_dotenv()

from src.common.exceptions import (
    DatabaseError,
    InexistentConnection,
    InexistentSQLFile,
)


class DBManager:
    _pool: pooling.MySQLConnectionPool | None = None

    def __init__(self) -> None:
        self.host: str = os.environ["DB_HOST"]
        self.user: str = os.environ["DB_USER"]

        if os.environ.get("TESTING") == "True":
            self.database: str = os.environ["DB_TEST_NAME"]
            self.port: int = int(os.environ["DB_TEST_PORT"])
            self.password: str = os.environ["DB_TEST_PASS"]
        else:
            self.database: str = os.environ["DB_NAME"]
            self.port: int = int(os.environ["DB_PORT"])
            self.password: str = os.environ["DB_PASS"]

        if DBManager._pool is None:
            self._initialize_pool()

    def _initialize_pool(self) -> None:
        try:
            DBManager._pool = pooling.MySQLConnectionPool(
                pool_name="app_pool",
                pool_size=10,
                pool_reset_session=True,
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
            )
        except Exception as e:
            raise DatabaseError(str(e)) from e

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if hasattr(self, "connection") and self.connection.is_connected():
            if exception_type is not None or os.environ.get("TESTING") == "True":
                self.connection.rollback()
            else:
                self.connection.commit()

            self.disconnect()

    def connect(self) -> None:
        if DBManager._pool is None:
            raise InexistentConnection()

        self.connection: PooledMySQLConnection = DBManager._pool.get_connection()

        if self.connection.is_connected():
            print("Connected.")
            self.cursor: MySQLCursor = cast(MySQLCursor, self.connection.cursor())

    def disconnect(self) -> None:
        if hasattr(self, "cursor") and self.cursor:
            self.cursor.close()
            del self.cursor

        if hasattr(self, "connection") and self.connection:
            self.connection.close()
            del self.connection

    def execute_sql_file(self, route: str) -> None:
        if not self.connection.is_connected():
            raise InexistentConnection

        try:
            with open(route, "r", encoding="utf-8") as f:
                lines: list[str] = f.read().split(";")

            for line in lines:
                if line.strip() != "":
                    self.cursor.execute(line)

        except FileNotFoundError as e:
            raise InexistentSQLFile from e

        except Exception as e:
            raise DatabaseError(str(e)) from e

    def execute_read(
        self, query: str, values: Sequence[Any] = ()
    ) -> list[tuple[Any, ...]]:
        if not self.connection.is_connected():
            raise InexistentConnection
        try:
            self.cursor.execute(query, values)
            rows = self.cursor.fetchall()
            return cast(list[tuple[Any, ...]], rows) if rows else []
        except Exception as e:
            raise DatabaseError(str(e)) from e

    def execute_read_single_column(
        self, query: str, values: Sequence[Any] = ()
    ) -> list[Any]:
        rows = self.execute_read(query, values)
        return [row[0] for row in rows]

    def execute_write(self, query: str, values: Sequence[Any] = ()) -> int:
        if not self.connection.is_connected():
            raise InexistentConnection
        try:
            self.cursor.execute(query, values)
            return self.cursor.rowcount
        except Exception as e:
            raise DatabaseError(str(e)) from e

    def execute_write_many(self, query: str, values: Sequence[Sequence[Any]]) -> int:
        if not self.connection.is_connected():
            raise InexistentConnection
        try:
            self.cursor.executemany(query, values)
            return self.cursor.rowcount
        except Exception as e:
            raise DatabaseError(str(e)) from e
