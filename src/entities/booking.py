from datetime import datetime
from decimal import Decimal
from uuid import UUID

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
            raise TypeError(f"The type of {value} is not UUID.")
        
        self._id = value

    @property
    def booking_reference(self) -> str:
        return self._booking_reference
    
    @booking_reference.setter
    def booking_reference(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"The type of {value} is not str.")
        
        if not value.strip():
            raise ValueError("The booking reference can not be empty.")
        
        if len(value.strip()) != 6:
            raise ValueError("The booking reference mut be 6 characters long.")
        
        self._booking_reference = value

    @property
    def booking_datetime(self) -> datetime:
        return self._booking_datetime
    
    @booking_datetime.setter
    def booking_datetime(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise TypeError(f"The type of {value} is not datetime.")
        
        self._booking_datetime = value

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

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "booking_reference": self.booking_reference,
            "booking_datetime": self.booking_datetime,
            "paid_amount_usd": self.paid_amount_usd,
            "current_status_id": self.current_status_id
        } 