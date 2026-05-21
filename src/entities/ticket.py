from decimal import Decimal
from uuid import UUID

class Ticket:

    def __init__(self,
                id: UUID,
                ticket_number: str,
                paid_amount_usd: Decimal,
                current_status_id: int,
                booking_id: UUID,
                flight_id: UUID,
                passenger_id: UUID) -> None:
        
        self.id = id
        self.ticket_number = ticket_number
        self.paid_amount_usd = paid_amount_usd
        self.current_status_id = current_status_id
        self.booking_id = booking_id
        self.flight_id = flight_id
        self.passenger_id = passenger_id
    
    @property
    def id(self) -> UUID:
        return self._id
    
    @id.setter
    def id(self, value: UUID) -> None:
        if not isinstance(value, UUID):
            raise TypeError(f"The type of {value} is not UUID.")
        
        self._id = value

    @property
    def ticket_number(self) -> str:
        return self._ticket_number
    
    @ticket_number.setter
    def ticket_number(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"The type of {value} is not str.")
        
        value = value.strip()
        
        if not value:
            raise ValueError("The ticket number can not be empty.")
        
        if len(value) != 13:
            raise ValueError("The ticket number must be exactly 13 characters long.")
        
        if not value.isnumeric():
            raise ValueError("The ticket number must only contain digits.")
        
        self._ticket_number = value

    @property
    def paid_amount_usd(self) -> Decimal:
        return self._paid_amount_usd
    
    @paid_amount_usd.setter
    def paid_amount_usd(self, value: Decimal) -> None:
        if not isinstance(value, Decimal):
            raise TypeError(f"The type of {value} is not decimal.")
        
        if value <= 0:
            raise ValueError("The paid amount can not be negative or zero.")
        
        self._paid_amount_usd = value

    @property
    def current_status_id(self) -> int:
        return self._current_status_id

    @current_status_id.setter
    def current_status_id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"The type of {value} is not int.")
        
        if value <= 0:
            raise ValueError(f"The current status id can not be negative or zero.")
        
        self._current_status_id = value

    @property
    def booking_id(self) -> UUID:
        return self._booking_id

    @booking_id.setter
    def booking_id(self, value: UUID) -> None:
        if not isinstance(value, UUID):
            raise TypeError(f"The type of {value} is not UUID.")
        
        self._booking_id = value

    @property
    def flight_id(self) -> UUID:
        return self._flight_id
    
    @flight_id.setter
    def flight_id(self, value: UUID) -> None:
        if not isinstance(value, UUID):
            raise TypeError(f"The type of {value} is not UUID.")
        
        self._flight_id = value

    @property
    def passenger_id(self) -> UUID:
        return self._passenger_id
    
    @passenger_id.setter
    def passenger_id(self, value: UUID) -> None:
        if not isinstance(value, UUID):
            raise TypeError(f"The type of {value} is not UUID.")
        
        self._passenger_id = value
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "ticket_number": self.ticket_number,
            "paid_amount_usd": self.paid_amount_usd,
            "current_status_id": self.current_status_id,
            "booking_id": self.booking_id,
            "flight_id": self.flight_id,
            "passenger_id": self.passenger_id
        }