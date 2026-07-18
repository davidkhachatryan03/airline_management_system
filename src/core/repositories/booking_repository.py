from src.common import DBManager
from src.common.types import BookingRow
from src.entities import Booking


class BookingRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager

    def insert_booking(self, booking: Booking) -> None:
        self.db_manager.insert_rows("bookings", [booking])

    def retrieve_bookings(self, limit: int = 5) -> list[Booking]:
        query = "SELECT id, booking_reference, booking_datetime, paid_amount_usd, current_status_id FROM bookings ORDER BY id DESC LIMIT %s"

        results: list[BookingRow] = self.db_manager.retrieve_many_columns(
            query, (limit,)
        )

        if results:
            return [Booking(*result) for result in results]

        return []
