from datetime import datetime
from decimal import Decimal

class BookingCreated:

    def __init__(self,
                booking_reference: str,
                booking_datetime: datetime,
                paid_amount_usd: Decimal,
                current_status_id: int) -> None:
        
        self.booking_reference = booking_reference
        self.booking_datetime = booking_datetime
        self.paid_amount_usd = paid_amount_usd
        self.current_status_id = current_status_id

    @property
    def booking_reference(self) -> str:
        return self._booking_reference
    
    @booking_reference.setter
    def booking_reference(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"The type of {value} is not str.")
        
        if not value.strip():
            raise ValueError("The booking reference can not be empty.")
        
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
        
        if value < 0:
            raise ValueError("The paid amount can not be negative or zero.")
        
        self._paid_amount_usd = value

    @property
    def current_status_id(self) -> int:
        return self._current_status_id

    @current_status_id.setter
    def current_status_id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"The type of {value} is not int.")
        
        if value < 0:
            raise ValueError(f"The current status id can not be negative or zero.")
        
        self._current_status_id = value

class BookingRetrieved:

    def __init__(self,
                id: int, 
                booking_reference: str,
                booking_datetime: datetime,
                paid_amount_usd: Decimal,
                current_status_id: int) -> None:
        
        self.id = id
        self.booking_reference = booking_reference
        self.booking_datetime = booking_datetime
        self.paid_amount_usd = paid_amount_usd
        self.current_status_id = current_status_id