from decimal import Decimal

class TicketCreated:

    def __init__(self,
                ticket_number: str,
                paid_amount_usd: Decimal,
                current_status_id: int,
                booking_id: int,
                flight_id: int,
                passenger_id: int) -> None:
        
        self.ticket_number = ticket_number
        self.paid_amount_usd = paid_amount_usd
        self.current_status_id = current_status_id
        self.booking_id = booking_id
        self.flight_id = flight_id
        self.passenger_id = passenger_id

    @property
    def ticket_number(self) -> str:
        return self._ticket_number
    
    @ticket_number.setter
    def ticket_number(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"The type of {value} is not str.")
        
        if not value.strip():
            raise ValueError("The ticket numbet can not be empty.")
        
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
    def booking_id(self) -> int:
        return self._booking_id

    @booking_id.setter
    def booking_id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"The type of {value} is not int.")
        
        if value <= 0:
            raise ValueError(f"The booking id can not be negative or zero.")
        
        self._booking_id = value

    @property
    def flight_id(self) -> int:
        return self._flight_id
    
    @flight_id.setter
    def flight_id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"The type of {value} is not int.")
        
        if value <= 0:
            raise ValueError(f"The flight id can not be negative or zero.")
        
        self._flight_id = value

    @property
    def passenger_id(self) -> int:
        return self._flight_id
    
    @passenger_id.setter
    def passenger_id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"The type of {value} is not int.")
        
        if value <= 0:
            raise ValueError(f"The passenger id can not be negative or zero.")
        
        self._passenger_id = value

class TicketRetrieved:

    def __init__(self,
                id: int,
                ticket_number: str,
                paid_amount_usd: Decimal,
                current_status_id: int,
                booking_id: int,
                flight_id: int,
                passenger_id: int) -> None:
        
        self.id = id
        self.ticket_number = ticket_number
        self.paid_amount_usd = paid_amount_usd
        self.current_status_id = current_status_id
        self.booking_id = booking_id
        self.flight_id = flight_id
        self.passenger_id = passenger_id