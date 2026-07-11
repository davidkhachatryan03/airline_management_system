# GENERAL EXCEPTIONS

class DatabaseError(Exception):
    status_code = 500
    def __init__(self, message) -> None:
        super().__init__(f"SQL Error: {message}")

class InvalidData(Exception):
    status_code = 400

class InexistentData(InvalidData):
    status_code = 404

class DuplicatedData(InvalidData):
    status_code = 409

# FLIGHT EXCEPTIONS

class InvalidFlight(InvalidData):
    pass 

class InexistentFlight(InvalidFlight, InexistentData):
    def __init__(self, message = "A flight is not available.") -> None:
        super().__init__(message)

class FullFlight(InvalidFlight):
    status_code = 409
    def __init__(self, message = "A flight is full.") -> None:
        super().__init__(message)

class NotScheduledFlight(InvalidFlight):
    status_code = 409
    def __init__(self, message = "A flight is not programmed.") -> None:
        super().__init__(message)

class InvalidFlightId(InvalidFlight):
    def __init__(self, message = "A flight's id is invalid.") -> None:
        super().__init__(message)

class DuplicatedFlight(InvalidFlight, DuplicatedData):
    def __init__(self, message = "The flight is already registered.") -> None:
        super().__init__(message)

# PASSENGER EXCEPTIONS

class InvalidPassenger(InvalidData):
    pass  

class InexistentPassenger(InvalidPassenger, InexistentData):
    def __init__(self, message = "The passenger is not registered.") -> None:
        super().__init__(message)

class BlacklistedPassenger(InvalidPassenger):
    status_code = 403
    def __init__(self, message = "A passenger is blacklisted.") -> None:
        super().__init__(message)

# DOCUMENT EXCEPTIONS

class InvalidDocument(InvalidData):
    pass  

class DuplicatedDocument(InvalidDocument, DuplicatedData):
    def __init__(self, message = "The document is already registered.") -> None:
        super().__init__(message)

# AIRPLANE EXCEPTIONS

class InvalidAirplane(InvalidData):
    pass  

class InexistentAirplane(InvalidAirplane, InexistentData):
    def __init__(self, message = "The selected airplane is not registered.") -> None:
        super().__init__(message)

class UnavailableAirplane(InvalidAirplane):
    status_code = 409
    def __init__(self, message = "The selected airplane is unavailable.") -> None:
        super().__init__(message)

# ROUTE EXCEPTIONS

class InvalidRoute(InvalidData):
    pass 

class InexistentRoute(InvalidRoute, InexistentData):
    def __init__(self, message = "The selected route is not registered.") -> None:
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

class InvalidBytes(DatabaseError):
    def __init__(self, message = "Bytes received not relates to UUID.") -> None:
        super().__init__(message)

# MULTIPLE EXCEPTIONS

class MultipleExceptionsError(Exception):
    def __init__(self, exceptions: list[Exception]) -> None:
        self.exceptions = exceptions