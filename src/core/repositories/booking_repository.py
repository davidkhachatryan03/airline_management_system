from typing import cast
from src.common import DBManager
from src.entities import Booking, Ticket

class BookingRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager  
        self.table_bookings = "bookings"
        self.table_tickets = "tickets"
    
    def insert_booking(self, booking_created: Booking, tickets_created: list[Ticket]) -> None:
        with self.db_manager:
            self.db_manager.insert_row(self.table_bookings, booking_created)

            for ticket_created in tickets_created:
                self.db_manager.insert_row(self.table_tickets, ticket_created)