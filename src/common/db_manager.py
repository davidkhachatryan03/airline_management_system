import mysql.connector, os
from dotenv import load_dotenv
from typing import Any, cast
from uuid import UUID

from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from src.common.exceptions import DatabaseError, InexistentConnection, InexistentSQLFile, InvalidBytes

load_dotenv()

class DBManager:

    def __init__(self) -> None:
        self.host: str = os.environ["DB_HOST"]
        self.user: str = os.environ["DB_USER"]
        self.password: str = os.environ["DB_PASS"]
        self.database: str = os.environ["DB_NAME"]

    def __enter__(self):
        self.connect()
        self.connection.autocommit = False
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if self.connection and self.connection.is_connected():
            if exception_type is not None:
                self.connection.rollback()
            else:
                self.connection.commit()
            
            self.disconnect()

    def connect(self) -> None:
        self.connection: MySQLConnection = cast(MySQLConnection, mysql.connector.connect(
            host = self.host,
            port = 3306,
            user = self.user,
            password = self.password,
            database = self.database
        ))

        if self.connection.is_connected():
            print("Connected.")
            self.cursor: MySQLCursor = cast(MySQLCursor, self.connection.cursor())
    
    def disconnect(self) -> None:
        if self.connection and self.cursor:
            self.connection.close()
            self.cursor.close()
            print("Disconnected.")

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
            raise DatabaseError(e) from e
    
    def retrieve_many_columns(self, query: str, values: tuple[Any, ...] | list[Any] = ()) -> list[tuple[Any, ...]]:
        if not self.connection.is_connected():
            raise InexistentConnection("Connection not found.")
        
        try:
            values_formatted: list = self.uuid_to_bytes(list(values))

            self.cursor.execute(query, values_formatted)
            rows: list[tuple] = cast(list[tuple], self.cursor.fetchall())

            if not rows:
                return []

            return self.bytes_to_uuid(rows)

        except Exception as e:
            raise DatabaseError(e) from e
        
    def retrieve_single_column(self, query: str, values: tuple[Any, ...] | list[Any] = ()) -> list[Any]:
        if not self.connection.is_connected():
            raise InexistentConnection("Connection not found.")
        
        try:
            values_formatted: list = self.uuid_to_bytes(list(values))

            self.cursor.execute(query, values_formatted)
            rows: list[tuple] = cast(list[tuple], self.cursor.fetchall())

            if not rows:
                return []

            result: list = [rows[i][0] for i in range(len(rows))]

            return self.bytes_to_uuid(result)

        except Exception as e:
            raise DatabaseError(e) from e
        
    def insert_rows(self, table_name: str, entities: list) -> int:
        if not self.connection.is_connected():
            raise InexistentConnection("Connection not found.")
        
        try:
            row: dict = entities[0].to_dict()
            
            columns: str = "(" + ",".join(row.keys()) + ")"
            columns_amount: str = "(" + ",".join(["%s"] * len(row)) + ")"

            values: list[list] = [list(entity.to_dict().values()) for entity in entities]
            values_formatted: list[list] = [self.uuid_to_bytes(value) for value in values]

            query = "INSERT INTO {} {} VALUES {}".format(table_name, columns, columns_amount)

            self.cursor.executemany(query, values_formatted)
            return cast(int, self.cursor.rowcount)
        
        except AttributeError as e:
            raise ValueError("The entity has not to_dict method.") from e
        
        except Exception as e:
            raise DatabaseError(e) from e
    
    def uuid_to_bytes(self, rows: list) -> list[bytes]:
        rows_formatted: list[bytes] = []

        for row in rows:
            if isinstance(row, UUID):
                rows_formatted.append(row.bytes)
            else:
                rows_formatted.append(row)
        
        return rows_formatted
    
    def bytes_to_uuid(self, rows: list) -> list:
        rows_formatted: list = []

        if not isinstance(rows[0], tuple):
            for row in rows:
                if isinstance(row, bytes) and len(row) == 16:
                    bytes_to_uuid: UUID = UUID(bytes=row)
                    if bytes_to_uuid.version != 7:
                        raise InvalidBytes
                    rows_formatted.append(bytes_to_uuid)
                else:
                    rows_formatted.append(row)
        
        else:
            for row in rows:
                row_formatted: list = []

                for element in row:
                    if isinstance(element, bytes) and len(element) == 16:
                        bytes_to_uuid: UUID = UUID(bytes=element)
                        if bytes_to_uuid.version != 7:
                            raise InvalidBytes
                        row_formatted.append(bytes_to_uuid)
                    else:
                        row_formatted.append(element)
                
                rows_formatted.append(tuple(row_formatted))
                
        return rows_formatted