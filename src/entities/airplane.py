from decimal import Decimal

class AirplaneCreated:

    def __init__(self, 
                tail_number: str, 
                manufacturer: str, 
                model: str,
                capacity: int,
                range_km: int,
                flight_hour_cost_usd: Decimal,
                current_status_id: int) -> None:
        
        self.tail_number = tail_number
        self.manufacturer = manufacturer
        self.model = model
        self.capacity = capacity
        self.range_km = range_km
        self.flight_hour_cost_usd = flight_hour_cost_usd
        self.current_status_id = current_status_id
    
    @property
    def tail_number(self) -> str:
        return self._tail_number
    
    @tail_number.setter
    def tail_number(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"The type of {value} is not str.")
        
        if not value.strip():
            raise ValueError(f"The tail number can not be empty.")
        
        self._tail_number = value

    @property
    def manufacturer(self) -> str:
        return self._manufacturer
    
    @manufacturer.setter
    def manufacturer(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"The type of {value} is not str.")
        
        if not value.strip():
            raise ValueError(f"The tail number can not be empty.")
        
        self._manufacturer = value

    @property
    def model(self) -> str:
        return self._model 
    
    @model.setter
    def model(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"The type of {value} is not str.")
        
        if not value.strip():
            raise ValueError(f"The tail number can not be empty.")
        
        self._model = value

    @property
    def capacity(self) -> int:
        return self._capacity
    
    @capacity.setter
    def capacity(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"The type of {value} is not int.")
        
        if value <= 0:
            raise ValueError(f"The capacity can not be negative or zero.")
        
        self._capacity = value

    @property
    def range_km(self) -> int:
        return self._range_km
    
    @range_km.setter
    def range_km(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"The type of {value} is not int.")
        
        if value <= 0:
            raise ValueError(f"The range can not be negative or zero.")
        
        self._range_km = value

    @property
    def flight_hour_cost_usd(self) -> Decimal:
        return self._flight_hour_cost
    
    @flight_hour_cost_usd.setter
    def flight_hour_cost_usd(self, value: Decimal) -> None:
        if not isinstance(value, Decimal):
            raise TypeError(f"The type of {value} is not decimal.")
        
        if value <= 0:
            raise ValueError(f"The flight hour cost can not be negative or zero.")
        
        self._flight_hour_cost = value

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

class AirplaneRetrieved:
    def __init__(self,
                id: int, 
                tail_number: str, 
                manufacturer: str, 
                model: str,
                capacity: int,
                range_km: int,
                flight_hour_cost_usd: Decimal,
                current_status_id: int) -> None:
        
        self.id = id
        self.tail_number = tail_number
        self.manufacturer = manufacturer
        self.model = model
        self.capacity = capacity
        self.range_km = range_km
        self.flight_hour_cost_usd = flight_hour_cost_usd
        self.current_status_usd = current_status_id