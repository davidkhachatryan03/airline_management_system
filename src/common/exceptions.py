class AirlineError(Exception):
    pass

class InvalidData(Exception):
    pass

class DatabaseError(AirlineError):
    pass

class CursorNotFound(DatabaseError):
    pass

class SQLFileNotFound(DatabaseError):
    pass

class NoConnection(DatabaseError):
    pass

class InsertionMissmatchError(DatabaseError):
    pass

class InvalidPassengerId(InvalidData):
    pass

class InvalidPassengerBlacklisted(InvalidData):
    pass

class InvalidBooking(InvalidData):
    pass

class InvalidFlightId(InvalidData):
    pass

class InvalidPaidAmountUsd(InvalidData):
    pass
