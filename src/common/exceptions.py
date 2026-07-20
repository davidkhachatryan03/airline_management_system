from collections.abc import Sequence
from uuid import UUID

from src.common.types import (
    AirplaneId,
    DocumentIdentityKey,
    FlightId,
    FlightIdentityKey,
    PassengerId,
    RouteId,
    RowIdentityKey,
)

# GENERAL EXCEPTIONS


class DatabaseError(Exception):
    status_code = 500

    def __init__(self, message: str) -> None:
        super().__init__(f"SQL Error: {message}")


class InvalidData(Exception):
    status_code = 400

    def __init__(self, id: int | UUID | RowIdentityKey, message: str) -> None:
        self.id = id
        super().__init__(message)


class InexistentData(InvalidData):
    status_code = 404


class DuplicatedData(InvalidData):
    status_code = 409


# FLIGHT EXCEPTIONS


class InvalidFlight(InvalidData):
    pass


class InexistentFlight(InexistentData, InvalidFlight):
    def __init__(self, id: FlightId) -> None:
        message = f"The flight with id {id} is not registered."
        super().__init__(id, message)


class FullFlight(InvalidFlight):
    status_code = 409

    def __init__(self, id: FlightId) -> None:
        message = f"The flight with id {id} is full."
        super().__init__(id, message)


class NotScheduledFlight(InvalidFlight):
    status_code = 409

    def __init__(self, id: FlightId) -> None:
        message = f"The flight with id {id} is not scheduled."
        super().__init__(id, message)


class DuplicatedFlight(DuplicatedData, InvalidFlight):
    def __init__(self, identity_key: FlightIdentityKey) -> None:
        message = f"The flight with id {identity_key} is already registered."
        super().__init__(identity_key, message)


class NotSeatsEnough(InvalidFlight):
    status_code = 409

    def __init__(self, id: FlightId) -> None:
        message = f"The flight with id {id} has not seats enough."
        super().__init__(id, message)


# PASSENGER EXCEPTIONS


class InvalidPassenger(InvalidData):
    pass


class InexistentPassenger(InexistentData, InvalidPassenger):
    def __init__(self, id: PassengerId) -> None:
        message = f"The passenger with id {id} is not registered."
        super().__init__(id, message)


class BlacklistedPassenger(InvalidPassenger):
    status_code = 403

    def __init__(self, id: PassengerId) -> None:
        message = f"The passenger with id {id} is blacklisted."
        super().__init__(id, message)


# DOCUMENT EXCEPTIONS


class InvalidDocument(InvalidData):
    pass


class DuplicatedDocument(DuplicatedData, InvalidDocument):
    def __init__(self, identity_key: DocumentIdentityKey) -> None:
        message = f"The document with id {identity_key} is already registered."
        super().__init__(identity_key, message)


# AIRPLANE EXCEPTIONS


class InvalidAirplane(InvalidData):
    pass


class InexistentAirplane(InexistentData, InvalidAirplane):
    def __init__(self, id: AirplaneId) -> None:
        message = f"The airplane with id {id} is not registered."
        super().__init__(id, message)


class UnavailableAirplane(InvalidAirplane):
    status_code = 409

    def __init__(self, id: AirplaneId) -> None:
        message = f"The airplane with id {id} is unavailable."
        super().__init__(id, message)


# ROUTE EXCEPTIONS


class InvalidRoute(InvalidData):
    pass


class InexistentRoute(InexistentData, InvalidRoute):
    def __init__(self, id: RouteId) -> None:
        message = f"The route with id {id} is not registered."
        super().__init__(id, message)


# DATABASE EXCEPTIONS


class InexistentDatabase(DatabaseError):
    pass


class InexistentSQLFile(DatabaseError):
    def __init__(self) -> None:
        message = "SQL file not found."
        super().__init__(message)


class InexistentConnection(DatabaseError):
    def __init__(self) -> None:
        message = "Connection not found"
        super().__init__(message)


class InvalidBytes(DatabaseError):
    def __init__(self) -> None:
        message = "Bytes received not relates to UUID."
        super().__init__(message)


# MULTIPLE EXCEPTIONS


class MultipleExceptionsError(Exception):
    def __init__(self, exceptions: Sequence[InvalidData]) -> None:
        self.exceptions = exceptions
