from src.common import DBManager
from src.entities import Booking

class BookingRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager

    def insert_booking(self, booking: Booking) -> None:
        self.db_manager.insert_rows("bookings", [booking])
    
    def retrieve_bookings(self, limit: int = 5) -> list[Booking]:
        query = "SELECT * FROM bookings ORDER BY id DESC LIMIT %s"

        results: list[tuple] = self.db_manager.retrieve(query, (limit,))

        return [Booking(*result) for result in results]