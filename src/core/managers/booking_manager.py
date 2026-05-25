import random, string, uuid6
from uuid import UUID
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from src.core.repositories import BookingRepository
from src.core.validators import BookingValidator
from src.entities import Booking, Ticket
from src.api.schemas import BookingResponse, BookingRequest
from src.common.exceptions import InvalidData

class BookingManager:

    def __init__(self, booking_repository: BookingRepository, booking_validator: BookingValidator) -> None:
        self.booking_repository = booking_repository
        self.booking_validator = booking_validator
    
    def process_booking(self, booking_request: BookingRequest) -> BookingResponse:
        self.booking_validator.validate_booking_request(booking_request)
        
        flights_id: list[UUID] = booking_request.flights_id
        passengers_id: list[UUID] = booking_request.passengers_id

        paid_amount_usd: Decimal = booking_request.paid_amount_usd
        paid_amount_usd_per_passenger: Decimal = (paid_amount_usd / len(passengers_id)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        booking_reference: str = self.generate_booking_reference()
        booking_id: UUID = uuid6.uuid7()
        booking_datetime: datetime = datetime.now()

        booking_created: Booking = self.generate_booking(booking_id, booking_reference, booking_datetime, paid_amount_usd)
        tickets_created: list[Ticket] = self.generate_tickets(passengers_id, flights_id, booking_id, paid_amount_usd_per_passenger)
        
        self.booking_repository.insert_booking(booking_created, tickets_created)

        booking_response: BookingResponse = self.generate_booking_response(booking_reference, tickets_created, booking_datetime, paid_amount_usd)

        return booking_response
    
    def generate_booking_reference(self) -> str:
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        digits = ''.join(random.choices(string.digits, k=3))
    
        return f"{letters}{digits}"
    
    def generate_ticket_number(self) -> str:
        digits = ''.join(random.choices(string.digits, k=13))

        return digits
    
    def generate_tickets(self, passengers_id: list[UUID], flights_id: list[UUID], booking_id: UUID, paid_amount_usd_per_passenger: Decimal) -> list[Ticket]:
        tickets_created: list[Ticket] = []
        for passenger_id in passengers_id:
            for flight_id in flights_id:
                ticket_number: str = self.generate_ticket_number()
                ticket_id: UUID = uuid6.uuid7()

                ticket_created = Ticket(
                    id=ticket_id,
                    ticket_number=ticket_number,
                    paid_amount_usd=paid_amount_usd_per_passenger,
                    current_status_id=1,
                    booking_id=booking_id,
                    flight_id=flight_id,
                    passenger_id=passenger_id
                )

                tickets_created.append(ticket_created)
        
        return tickets_created
    
    def generate_booking_response(self, booking_reference: str, tickets: list[Ticket], booking_datetime: datetime, paid_amount_usd: Decimal) -> BookingResponse:
        return BookingResponse(
            booking_reference=booking_reference,
            tickets=[ticket.ticket_number for ticket in tickets],
            booking_datetime=booking_datetime,
            paid_amount_usd=paid_amount_usd,
            current_status_id=1
        )
    
    def generate_booking(self, id: UUID, booking_reference: str, booking_datetime: datetime, paid_amount_usd: Decimal) -> Booking:
        return Booking(
            id=id,
            booking_reference=booking_reference,
            booking_datetime=booking_datetime,
            paid_amount_usd=paid_amount_usd,
            current_status_id=1
        )