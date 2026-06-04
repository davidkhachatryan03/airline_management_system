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
        
        value_formatted: str = value.strip()
        
        if not value_formatted:
            raise ValueError(f"The tail number can not be empty.")
        
        if len(value_formatted) > 10:
            raise ValueError("The tail number must be 10 characters or less.")
        
        self._tail_number = value_formatted

    @property
    def manufacturer(self) -> str:
        return self._manufacturer
    
    @manufacturer.setter
    def manufacturer(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"The type of {value} is not str.")
        
        value_formatted: str = value.strip()
        
        if not value_formatted:
            raise ValueError(f"The manufacturer can not be empty.")
        
        if len(value_formatted) > 50:
            raise ValueError("The manufacturer must be 50 characters or less.")
        
        self._manufacturer = value_formatted

    @property
    def model(self) -> str:
        return self._model 
    
    @model.setter
    def model(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"The type of {value} is not str.")
        
        value_formatted: str = value.strip()
        
        if not value_formatted:
            raise ValueError(f"The tail number can not be empty.")
        
        if len(value_formatted) > 50:
            raise ValueError("The tail number must be 50 characters or less.")
        
        self._model = value_formatted

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
    
    def to_dict(self) -> dict:
        return {
            "tail_number": self.tail_number,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "capacity": self.capacity,
            "range_km": self.range_km,
            "flight_hour_cost_usd": self.flight_hour_cost_usd,
            "current_status_id": self.current_status_id
        }

class AirplaneRetrieved(AirplaneCreated):
    
    def __init__(self,
                id: int, 
                tail_number: str, 
                manufacturer: str, 
                model: str,
                capacity: int,
                range_km: int,
                flight_hour_cost_usd: Decimal,
                current_status_id: int) -> None:
        
        super().__init__(tail_number, 
                        manufacturer, 
                        model, 
                        capacity, 
                        range_km, 
                        flight_hour_cost_usd, 
                        current_status_id)
        
        self.id = id

    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"The type the id is not int.")
        
        if value <= 0:
            raise ValueError(f"The id can not be negative or zero.")
        
        self._current_status_id = value
        
        self._id = value

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "tail_number": self.tail_number,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "capacity": self.capacity,
            "range_km": self.range_km,
            "flight_hour_cost_usd": self.flight_hour_cost_usd,
            "current_status_id": self.current_status_id
        }