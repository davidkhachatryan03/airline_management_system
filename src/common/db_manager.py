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

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exception_type, exception_value , exception_traceback):
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
            raise DatabaseError(f"The selected database does not exist.") from e

    def execute_sql_file(self, route: str) -> None:
        if not self.connection.is_connected():
            raise NoConnection("Connection not found.")

        try:
            with open(route, "r", encoding="utf-8") as f:
                lines: list[str] = f.read().split(";")

            for line in lines:
                self.cursor.execute(line)

        except FileNotFoundError as e:
            raise SQLFileNotFound("SQL file not found.") from e
        
        except PermissionError as e:
            raise DatabaseError("Access to file is not granted.") from e

        except Exception as e:
            raise DatabaseError(f"SQL error: {e} ") from e
    
    def retrieve(self, query: str, values: tuple | list = ()) -> list:
        if not self.connection.is_connected():
            raise NoConnection("Connection not found.")
        
        try:
            self.cursor.execute(query, values)
            rows: list[tuple] = cast(list[tuple], self.cursor.fetchall())

            if not rows:
                return []
            
            if len(rows[0]) == 1:
                return [rows[i][0] for i in range(len(rows))]
            
            return rows

        except Exception as e:
            self.disconnect()
            raise DatabaseError(f"SQL error: {e}") from e
        
    def insert_row(self, table_name: str, entity) -> int:
        if not self.connection.is_connected():
            raise NoConnection("Connection not found.")
        
        try:
            row: dict = entity.to_dict()
            
            columns: str = "(" + ",".join(row.keys()) + ")"
            columns_amount: str = "(" + ",".join(["%s"] * len(row)) + ")"

            values: list = list(row.values())

            query = "INSERT INTO {} {} VALUES {}".format(table_name, columns, columns_amount)

            self.cursor.execute(query, values)
            return cast(int, self.cursor.lastrowid)
        
        except AttributeError as e:
            raise ValueError("The entity has not to_dict method.") from e
        
        except Exception as e:
            raise DatabaseError(f"SQL error: {e}") from e