from typing import cast
import mysql.connector, os
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from dotenv import load_dotenv
from exceptions import CursorNotFound, DatabaseError, SQLFileNotFound

load_dotenv()

class DBManager:

    def __init__(self) -> None:
        self.host: str = os.environ["DB_HOST"]
        self.user: str = os.environ["DB_USER"]
        self.password: str = os.environ["DB_PASS"]

    def connect(self) -> None:
        self.conexion: MySQLConnection = cast(MySQLConnection, mysql.connector.connect(
            host = self.host,
            port = 3306,
            user = self.user,
            password = self.password
        ))

        if self.conexion.is_connected():
            print("Connected.")
            self.cursor: MySQLCursor = cast(MySQLCursor, self.conexion.cursor)
    
    def disconnect(self) -> None:
        if self.conexion and self.cursor:
            self.conexion.close()
            self.cursor.close()
            print("Disconnected.")

    def execute_sql_file(self, route: str) -> None:
        if self.cursor is None:
            raise CursorNotFound("Cursor not found.")

        try:
            with open(route, "r", encoding="utf-8") as f:
                lines: list[str] = f.read().split(";")

        except FileNotFoundError as e:
            raise SQLFileNotFound("SQL file not found.") from e
        
        except PermissionError as e:
            raise DatabaseError("Access to file is not granted.") from e

        try:
            for line in lines:
                self.cursor.execute(line)

        except Exception as e:
            raise DatabaseError(f"SQL error: {e} ") from e
    
    def retrieve(self, query: str, values: tuple | list | None = None) -> list[tuple]:
        if self.cursor is None:
            raise CursorNotFound("Cursor not found.")
        
        try:
            self.cursor.execute(query, values)
            results: list[tuple] = cast(list[tuple], self.cursor.fetchall())
            return results

        except Exception as e:
            raise DatabaseError(f"SQL error: {e}") from e
        
    def insert_row(self, table_name: str, row: dict) -> None:
        if self.cursor is None:
            raise CursorNotFound("Cursor not found.")
        
        columns: str = "(" + ",".join(row.keys()) + ")"
        columns_amount: str = "(" + ",".join(["%s"] * len(row)) + ")"

        values: list = list(row.values())

        query = "INSERT INTO {} {} VALUES {}".format(table_name, columns, columns_amount)

        try:
            self.cursor.execute(query, values)
            self.conexion.commit()
        
        except Exception as e:
            raise DatabaseError(f"SQL error: {e}") from e