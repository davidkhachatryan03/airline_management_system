from src.common import DBManager
from src.core.repositories.base_repository import BaseRepository
from src.entities import Booking, Document, Passenger, Ticket


class BookingRepository(BaseRepository[Booking]):

    def __init__(self, db_manager: DBManager) -> None:
        super().__init__(
            db_manager,
            "bookings",
            (
                "id",
                "booking_reference",
                "booking_datetime",
                "paid_amount_usd",
                "current_status_id",
            ),
            Booking,
        )


class DocumentRepository(BaseRepository[Document]):

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager
        super().__init__(
            db_manager,
            "documents",
            (
                "id",
                "document_number",
                "valid_from",
                "valid_until",
                "issue_country",
                "passenger_id",
                "document_type_id",
            ),
            Document,
            ("document_number", "issue_country"),
        )


class TicketRepository(BaseRepository[Ticket]):

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager
        super().__init__(
            db_manager,
            "tickets",
            (
                "id",
                "ticket_number",
                "paid_amount_usd",
                "current_status_id",
                "booking_id",
                "flight_id",
                "passenger_id",
            ),
            Ticket,
        )
