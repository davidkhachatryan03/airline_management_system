from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID

import uuid6

from src.common.types import DurationMin
from src.entities.base_entity import BaseEntity


class Flight(BaseEntity):

    def __init__(self,
                id: UUID,
                scheduled_departure_datetime: datetime,
                scheduled_arrival_datetime: datetime,
                actual_departure_datetime: datetime | None,
                actual_arrival_datetime: datetime | None,
                operating_cost_usd: Decimal,
                base_price_usd: Decimal,
                current_status_id: int,
                route_id: int,
                airplane_id: int) -> None:
        
        self.id = id
        self.scheduled_departure_datetime = scheduled_departure_datetime
        self.scheduled_arrival_datetime = scheduled_arrival_datetime
        self.actual_departure_datetime = actual_departure_datetime
        self.actual_arrival_datetime = actual_arrival_datetime
        self.operating_cost_usd = operating_cost_usd
        self.base_price_usd = base_price_usd
        self.current_status_id = current_status_id
        self.route_id = route_id
        self.airplane_id = airplane_id

    @property
    def id(self) -> UUID:
        return self._id
    
    @id.setter
    def id(self, value: UUID) -> None:
        if not isinstance(value, UUID):
            raise TypeError("The type of the id is not UUID.")
        
        self._id = value

    @property
    def scheduled_departure_datetime(self) -> datetime:
        return self._scheduled_departure_datetime
    
    @scheduled_departure_datetime.setter
    def scheduled_departure_datetime(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise TypeError("The type of the scheduled departure datetime must be datetime or none.")
        
        self._scheduled_departure_datetime = value

    @property
    def scheduled_arrival_datetime(self) -> datetime:
        return self._scheduled_arrival_datetime
    
    @scheduled_arrival_datetime.setter
    def scheduled_arrival_datetime(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise TypeError("The type of the scheduled arrival datetime must be datetime or none.")
        
        self._scheduled_arrival_datetime = value

    @property
    def actual_departure_datetime(self) -> datetime | None:
        return self._actual_departure_datetime
    
    @actual_departure_datetime.setter
    def actual_departure_datetime(self, value: datetime | None) -> None:
        if value is not None and not isinstance(value, datetime):
            raise TypeError("The type of the actual departure datetime must be datetime or none.")
        
        self._actual_departure_datetime = value

    @property
    def actual_arrival_datetime(self) -> datetime | None:
        return self._actual_arrival_datetime
    
    @actual_arrival_datetime.setter
    def actual_arrival_datetime(self, value: datetime | None) -> None:
        if value is not None and not isinstance(value, datetime):
            raise TypeError("The type of the actual arrival datetime must be datetime or none.")
        
        self._actual_arrival_datetime = value

    @property
    def operating_cost_usd(self) -> Decimal:
        return self._operating_cost_usd
    
    @operating_cost_usd.setter
    def operating_cost_usd(self, value: Decimal) -> None:
        if not isinstance(value, Decimal):
            raise TypeError("The type of the operating cost is not datetime.")
        
        if value <= 0:
            raise ValueError("The operating cost can not be negative or zero.")
        
        self._operating_cost_usd = value
    
    @property
    def base_price_usd(self) -> Decimal:
        return self._base_price_usd
    
    @base_price_usd.setter
    def base_price_usd(self, value: Decimal) -> None:
        if not isinstance(value, Decimal):
            raise TypeError("The type of the base price is not decimal.")
        
        if value <= 0:
            raise ValueError("The base price can not be negative or zero.")
        
        self._base_price_usd = value

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

    @property
    def route_id(self) -> int:
        return self._route_id
    
    @route_id.setter
    def route_id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("The type of the route id is not int.")
        
        if value <= 0:
            raise ValueError("The route id can not be negative or zero.")
        
        self._route_id = value

    @property
    def airplane_id(self) -> int:
        return self._airplane_id
    
    @airplane_id.setter
    def airplane_id(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("The type of the airplane id is not int.")
        
        if value <= 0:
            raise ValueError("The airplane id can not be negative or zero.")
        
        self._airplane_id = value
    
    @property
    def identity_key(self) -> tuple[datetime, int]:
        return (self.scheduled_departure_datetime, self.route_id)
    
    @classmethod
    def new_flight(cls, 
                scheduled_departure_datetime: datetime, 
                scheduled_arrival_datetime: datetime,
                operating_cost_usd: Decimal,
                route_id: int,
                airplane_id: int) -> 'Flight':
        
        return cls(
            id=uuid6.uuid7(),
            scheduled_departure_datetime=scheduled_departure_datetime,
            scheduled_arrival_datetime=scheduled_arrival_datetime,
            actual_departure_datetime=None,
            actual_arrival_datetime=None,
            operating_cost_usd=operating_cost_usd,
            base_price_usd=cls._calculate_base_price_usd(operating_cost_usd),
            current_status_id=1,
            route_id=route_id,
            airplane_id=airplane_id
        )
    
    @staticmethod
    def _calculate_base_price_usd(operating_cost_usd: Decimal) -> Decimal:
        return (operating_cost_usd * Decimal("1.30")).quantize(Decimal("0.01"), ROUND_HALF_UP)
    
    @staticmethod
    def _calculate_operating_cost_usd(flight_hour_cost_usd: Decimal, duration_min: DurationMin) -> Decimal:
        return (flight_hour_cost_usd * (duration_min / Decimal("60"))).quantize(Decimal("0.01"), ROUND_HALF_UP)