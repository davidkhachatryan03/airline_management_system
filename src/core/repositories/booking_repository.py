from src.common import DBManager
from src.entities import Booking, Ticket
from uuid import UUID
from decimal import Decimal, ROUND_HALF_UP
from src.entities import Flight, Passenger

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
    
    def retrieve_passenger(self, passenger_id: UUID) -> Passenger:
        result = Passenger(*self.db_manager.retrieve("SELECT * FROM passengers WHERE id = %s", (passenger_id,))[0])

        return result
    
    def retrieve_flight(self, flight_id: UUID) -> Flight:
        result = Flight(*self.db_manager.retrieve("SELECT * FROM flight WHERE id = %s", (flight_id,))[0])

        return result
    
    def retrieve_paid_amount_usd(self, flight_id: UUID, pasengers_number: int) -> Decimal:
        query = """
                SELECT  r.distance_km, 
                        a.flight_hour_cost_usd
                FROM    flight f
                JOIN    route r
                ON      f.route_id = r.id
                JOIN    airplanes a
                ON      f.airplane_id = a.id
                WHERE   f.id = %s
                """

        result: list[tuple[int, Decimal]] = self.db_manager.retrieve(query, (flight_id,))

        return (result[0][0] * result[0][1] * pasengers_number).quantize(Decimal("0.01") ,rounding=ROUND_HALF_UP)