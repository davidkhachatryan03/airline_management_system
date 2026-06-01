# GENERAL EXCEPTIONS

class DatabaseError(Exception):
    def __init__(self, message) -> None:
        super().__init__(f"SQL Error: {message}")

class InvalidData(Exception):
    pass

# FLIGHT EXCEPTIONS

class InvalidFlight(InvalidData):
    pass

class InexistentFlight(InvalidFlight):
    pass

class FullFlight(InvalidFlight):
    def __init__(self, message = "A flight is full.") -> None:
        super().__init__(message)

class NotProgrammedFlight(InvalidFlight):
    def __init__(self, message = "A flight is not programmed.") -> None:
        super().__init__(message)

class InvalidFlightId(InvalidFlight):
    def __init__(self, message = "A flight's id is invalid.") -> None:
        super().__init__(message)

# PASSENGER EXCEPTIONS

class InvalidPassenger(InvalidData):
    pass

class BlacklistedPassenger(InvalidPassenger):
    def __init__(self, message = "A passenger is blacklisted.") -> None:
        super().__init__(message)

# DATABASE EXCEPTIONS

class InexistentDatabase(DatabaseError):
    pass

class InexistentSQLFile(DatabaseError):
    def __init__(self, message = "SQL file not found.") -> None:
        super().__init__(message)

class InexistentConnection(DatabaseError):
    def __init__(self, message = "Connection not found") -> None:
        super().__init__(message)