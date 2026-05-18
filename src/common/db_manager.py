from typing import cast
import mysql.connector, os
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from dotenv import load_dotenv
from src.common.exceptions import CursorNotFound, DatabaseError, SQLFileNotFound, NoConnection

load_dotenv()

class DBManager:

    def __init__(self) -> None:
        self.host: str = os.environ["DB_HOST"]
        self.user: str = os.environ["DB_USER"]
        self.password: str = os.environ["DB_PASS"]

    def connect(self) -> None:
        self.connection: MySQLConnection = cast(MySQLConnection, mysql.connector.connect(
            host = self.host,
            port = 3306,
            user = self.user,
            password = self.password
        ))

        if self.connection.is_connected():
            print("Connected.")
            self.cursor: MySQLCursor = cast(MySQLCursor, self.connection.cursor())
    
    def disconnect(self) -> None:
        if self.connection and self.cursor:
            self.connection.close()
            self.cursor.close()
            print("Disconnected.")
    
    def choose_database(self, database_name: str) -> None:
        try:
            self.cursor.execute("USE {}".format(database_name))
        
        except Exception as e:
            raise DatabaseError(f"SQL error: {e}") from e

    def execute_sql_file(self, route: str) -> None:
        if not self.connection.is_connected():
            raise NoConnection("Connection not found.")

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
    
    def retrieve(self, query: str, values: tuple | list | None = None) -> list[tuple] | tuple:
        if not self.connection.is_connected():
            raise NoConnection("Connection not found.")
        
        try:
            self.cursor.execute(query, values)
            results: list[tuple] = cast(list[tuple], self.cursor.fetchall())
            if len(results) > 1:
                return results
            return results[0]

        except Exception as e:
            raise DatabaseError(f"SQL error: {e}") from e
        
    def insert_row(self, table_name: str, entity) -> int:
        if not self.connection.is_connected():
            raise NoConnection("Connection not found.")
        
        row: dict = entity.to_dict()
        
        columns: str = "(" + ",".join(row.keys()) + ")"
        columns_amount: str = "(" + ",".join(["%s"] * len(row)) + ")"

        values: list = list(row.values())

        query = "INSERT INTO {} {} VALUES {}".format(table_name, columns, columns_amount)

        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return cast(int, self.cursor.lastrowid)
        
        except Exception as e:
            raise DatabaseError(f"SQL error: {e}") from e