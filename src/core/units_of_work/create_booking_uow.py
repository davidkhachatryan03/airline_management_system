from src.core.repositories import PassengerRepository, DocumentRepository, FlightRepository, BookingRepository, TicketRepository
from src.common import DBManager

class CreateBookingUoW:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager
        self.passenger_repository = PassengerRepository(self.db_manager)
        self.document_repository = DocumentRepository(self.db_manager)
        self.flight_repository = FlightRepository(self.db_manager)
        self.booking_repository = BookingRepository(self.db_manager)
        self.ticket_repository = TicketRepository(self.db_manager)

    def __enter__(self):
        self.db_manager.__enter__()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        return self.db_manager.__exit__(exception_type, exception_value, traceback)