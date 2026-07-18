from src.common import DBManager
from src.core.repositories import (
    BookingRepository,
    DocumentRepository,
    FlightRepository,
    PassengerRepository,
    TicketRepository,
)


class RegisterBookingUoW:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager
        self.passenger_repository = PassengerRepository(db_manager)
        self.document_repository = DocumentRepository(db_manager)
        self.flight_repository = FlightRepository(db_manager)
        self.booking_repository = BookingRepository(db_manager)
        self.ticket_repository = TicketRepository(db_manager)

    def __enter__(self):
        self.db_manager.__enter__()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        return self.db_manager.__exit__(exception_type, exception_value, traceback)
