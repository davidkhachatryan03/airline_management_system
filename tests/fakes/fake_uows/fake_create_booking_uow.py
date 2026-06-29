from tests.fakes.fake_db_manager import FakeDBManager
from tests.fakes.fake_repositories import FakeBookingRepository, FakeDocumentRepository, FakeFlightRepository, FakePassengerRepository, FakeTicketRepository

class FakeCreateBookingUoW:

    def __init__(self, db_manager: FakeDBManager) -> None:
        self.db_manager = db_manager
        self.passenger_repository = FakePassengerRepository()
        self.document_repository = FakeDocumentRepository()
        self.flight_repository = FakeFlightRepository()
        self.booking_repository = FakeBookingRepository()
        self.ticket_repository = FakeTicketRepository()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        pass