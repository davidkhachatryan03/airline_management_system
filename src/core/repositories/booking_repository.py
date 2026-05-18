from typing import cast
from common import DBManager
from common.rows import BookingRow
from entities import BookingCreated, BookingRetrieved

class BookingRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager  
        self.table_name = "bookings"
    
    def insert_booking(self, booking_created: BookingCreated) -> int:
        inserted_booking_id: int = self.db_manager.insert_row(self.table_name, booking_created)

        return inserted_booking_id