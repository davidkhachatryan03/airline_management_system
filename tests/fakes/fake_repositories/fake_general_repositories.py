from src.entities import Booking, Document, Passenger, Ticket
from tests.fakes.fake_repositories.fake_base_repository import \
    FakeBaseRepository


class FakeBookingRepository(FakeBaseRepository[Booking]):

    def __init__(self) -> None:
        super().__init__()


class FakeDocumentRepository(FakeBaseRepository[Document]):

    def __init__(self) -> None:
        super().__init__(("document_number", "issue_country"))


class FakePassengerRepository(FakeBaseRepository[Passenger]):

    def __init__(self) -> None:
        super().__init__()


class FakeTicketRepository(FakeBaseRepository[Ticket]):

    def __init__(self) -> None:
        super().__init__()
