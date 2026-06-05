from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID
from src.entities.flight import Flight
from src.entities.ticket import Ticket
import uuid6, string, random

class Booking:

    def __init__(self,
                id: UUID,
                booking_reference: str,
                booking_datetime: datetime,
                paid_amount_usd: Decimal,
                current_status_id: int) -> None:
        
        self.id = id
        self.booking_reference = booking_reference
        self.booking_datetime = booking_datetime
        self.paid_amount_usd = paid_amount_usd
        self.current_status_id = current_status_id
    
    @property
    def id(self) -> UUID:
        return self._id
    
    @id.setter
    def id(self, value: UUID) -> None:
        if not isinstance(value, UUID):
            raise TypeError("The type of the id is not UUID.")
        
        self._id = value

    @property
    def booking_reference(self) -> str:
        return self._booking_reference
    
    @booking_reference.setter
    def booking_reference(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("The type of the booking reference is not str.")
        
        value_formatted: str = value.strip()
        
        if not value_formatted:
            raise ValueError("The booking reference can not be empty.")
        
        if len(value_formatted) != 6:
            raise ValueError("The booking reference mut be 6 characters long.")
        
        self._booking_reference = value_formatted

    @property
    def booking_datetime(self) -> datetime:
        return self._booking_datetime
    
    @booking_datetime.setter
    def booking_datetime(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise TypeError("The type of the booking datetime is not datetime.")
        
        self._booking_datetime = value

    @property
    def paid_amount_usd(self) -> Decimal:
        return self._paid_amount_usd
    
    @paid_amount_usd.setter
    def paid_amount_usd(self, value: Decimal) -> None:
        if not isinstance(value, Decimal):
            raise TypeError("The type of the paid amount is not decimal.")
        
        if value <= 0:
            raise ValueError("The paid amount can not be negative or zero.")
        
        self._paid_amount_usd = value

    @property
    def current_status_id(self) -> int:
        return self._current_status_id

    @current_status_id.setter
    def current_status_id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("The type of the current status id is not int.")
        
        if value <= 0:
            raise ValueError("The current status id can not be negative or zero.")
        
        self._current_status_id = value
    
    def generate_tickets(self, passengers_id: list[UUID], flights: list[Flight], booking_id: UUID) -> list[Ticket]:
        tickets_created: list[Ticket] = []
        
        for passenger_id in passengers_id:
            for flight in flights: 
                ticket_created = Ticket.new_ticket(
                    paid_amount_usd=flight.base_price_usd,
                    booking_id=booking_id,
                    flight_id=flight.id,
                    passenger_id=passenger_id
                )
                
                tickets_created.append(ticket_created)
        
        return tickets_created

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "booking_reference": self.booking_reference,
            "booking_datetime": self.booking_datetime,
            "paid_amount_usd": self.paid_amount_usd,
            "current_status_id": self.current_status_id
        }
    
    @classmethod
    def new_booking(cls, flights: list[Flight], number_of_passengers: int) -> 'Booking':
        return cls(
            id=uuid6.uuid7(),
            booking_reference=cls._generate_reference(),
            booking_datetime=datetime.now(),
            paid_amount_usd=cls._calculate_paid_amount_usd(flights, number_of_passengers),
            current_status_id=1 
        )
    
    @staticmethod
    def _generate_reference() -> str:
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choices(chars, k=6))

    @staticmethod
    def _calculate_paid_amount_usd(flights: list[Flight], number_of_passengers: int) -> Decimal:
        paid_amount_usd: Decimal = (sum((flight.base_price_usd for flight in flights), Decimal("0")) * number_of_passengers).quantize(Decimal("0.01"), ROUND_HALF_UP)

        return paid_amount_usd