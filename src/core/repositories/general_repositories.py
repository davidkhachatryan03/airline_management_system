from src.common import DBManager
from src.core.repositories.base_repository import BaseRepository
from src.entities import Booking, Document, Ticket


class BookingRepository(BaseRepository[Booking]):

    def __init__(self, db_manager: DBManager) -> None:
        super().__init__(
            db_manager=db_manager,
            table_name="bookings",
            columns=(
                "id",
                "booking_reference",
                "booking_datetime",
                "paid_amount_usd",
                "current_status_id",
            ),
            entity=Booking,
            uuid_columns=tuple("id"),
        )


class DocumentRepository(BaseRepository[Document]):

    def __init__(self, db_manager: DBManager) -> None:
        super().__init__(
            db_manager=db_manager,
            table_name="documents",
            columns=(
                "id",
                "document_number",
                "valid_from",
                "valid_until",
                "issue_country",
                "passenger_id",
                "document_type_id",
            ),
            entity=Document,
            identity_key=("document_number", "issue_country"),
            uuid_columns=("id", "passenger_id"),
        )


class TicketRepository(BaseRepository[Ticket]):

    def __init__(self, db_manager: DBManager) -> None:
        super().__init__(
            db_manager=db_manager,
            table_name="tickets",
            columns=(
                "id",
                "ticket_number",
                "paid_amount_usd",
                "current_status_id",
                "booking_id",
                "flight_id",
                "passenger_id",
            ),
            entity=Ticket,
            uuid_columns=("id", "booking_id", "flight_id", "passenger_id"),
        )
