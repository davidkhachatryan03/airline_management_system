class AirlineError(Exception):
    pass

class DatabaseError(AirlineError):
    pass

class CursorNotFound(DatabaseError):
    pass

class SQLFileNotFound(DatabaseError):
    pass

class NoConnection(DatabaseError):
    pass