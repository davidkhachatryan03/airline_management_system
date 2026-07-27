from src.common.types import (
    AirplaneId,
    Capacity,
    CurrentStatusId,
    FlightHourCostUsd,
    Manufacturer,
    Model,
    RangeKm,
    TailNumber,
)
from src.entities.base_entity import BaseEntity


class Airplane(BaseEntity):

    def __init__(
        self,
        id: AirplaneId,
        tail_number: TailNumber,
        manufacturer: Manufacturer,
        model: Model,
        capacity: Capacity,
        range_km: RangeKm,
        flight_hour_cost_usd: FlightHourCostUsd,
        current_status_id: CurrentStatusId,
    ) -> None:

        self.id = id
        self.tail_number = tail_number
        self.manufacturer = manufacturer
        self.model = model
        self.capacity = capacity
        self.range_km = range_km
        self.flight_hour_cost_usd = flight_hour_cost_usd
        self.current_status_id = current_status_id

    @property
    def id(self) -> AirplaneId:
        return self._id

    @id.setter
    def id(self, value: AirplaneId) -> None:
        if not isinstance(value, AirplaneId.__value__):
            raise TypeError(f"The type the id is not int.")

        if value <= 0:
            raise ValueError(f"The id can not be negative or zero.")

        self._id = value

    @property
    def tail_number(self) -> TailNumber:
        return self._tail_number

    @tail_number.setter
    def tail_number(self, value: TailNumber) -> None:
        if not isinstance(value, TailNumber.__value__):
            raise TypeError(f"The type of {value} is not str.")

        value_formatted: TailNumber = value.strip()

        if not value_formatted:
            raise ValueError(f"The tail number can not be empty.")

        if len(value_formatted) > 10:
            raise ValueError("The tail number must be 10 characters or less.")

        self._tail_number = value_formatted

    @property
    def manufacturer(self) -> Manufacturer:
        return self._manufacturer

    @manufacturer.setter
    def manufacturer(self, value: Manufacturer) -> None:
        if not isinstance(value, Manufacturer.__value__):
            raise TypeError(f"The type of {value} is not str.")

        value_formatted: Manufacturer = value.strip()

        if not value_formatted:
            raise ValueError(f"The manufacturer can not be empty.")

        if len(value_formatted) > 50:
            raise ValueError("The manufacturer must be 50 characters or less.")

        self._manufacturer = value_formatted

    @property
    def model(self) -> Model:
        return self._model

    @model.setter
    def model(self, value: Model) -> None:
        if not isinstance(value, Model.__value__):
            raise TypeError(f"The type of {value} is not str.")

        value_formatted: Model = value.strip()

        if not value_formatted:
            raise ValueError(f"The model can not be empty.")

        if len(value_formatted) > 50:
            raise ValueError("The model must be 50 characters or less.")

        self._model = value_formatted

    @property
    def capacity(self) -> Capacity:
        return self._capacity

    @capacity.setter
    def capacity(self, value: Capacity) -> None:
        if not isinstance(value, Capacity.__value__):
            raise TypeError(f"The type of {value} is not int.")

        if value <= 0:
            raise ValueError(f"The capacity can not be negative or zero.")

        self._capacity = value

    @property
    def range_km(self) -> RangeKm:
        return self._range_km

    @range_km.setter
    def range_km(self, value: RangeKm) -> None:
        if not isinstance(value, RangeKm.__value__):
            raise TypeError(f"The type of {value} is not int.")

        if value <= 0:
            raise ValueError(f"The range can not be negative or zero.")

        self._range_km = value

    @property
    def flight_hour_cost_usd(self) -> FlightHourCostUsd:
        return self._flight_hour_cost

    @flight_hour_cost_usd.setter
    def flight_hour_cost_usd(self, value: FlightHourCostUsd) -> None:
        if not isinstance(value, FlightHourCostUsd.__value__):
            raise TypeError(f"The type of {value} is not decimal.")

        if value <= 0:
            raise ValueError(f"The flight hour cost can not be negative or zero.")

        self._flight_hour_cost = value

    @property
    def current_status_id(self) -> CurrentStatusId:
        return self._current_status_id

    @current_status_id.setter
    def current_status_id(self, value: CurrentStatusId) -> None:
        if not isinstance(value, CurrentStatusId.__value__):
            raise TypeError(f"The type of {value} is not int.")

        if value <= 0:
            raise ValueError(f"The current status id can not be negative or zero.")

        self._current_status_id = value
