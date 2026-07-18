from src.entities.base_entity import BaseEntity


class Route(BaseEntity):

    def __init__(
        self,
        id: int,
        flight_number: str,
        origin: str,
        destination: str,
        distance_km: int,
        duration_min: int,
    ) -> None:

        self.id = id
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.distance_km = distance_km
        self.duration_min = duration_min

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

    @property
    def flight_number(self) -> str:
        return self._flight_number

    @flight_number.setter
    def flight_number(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"The type of {value} is not str.")

        if not value.strip():
            raise ValueError("The flight number can not be empty.")

        if len(value.strip()) != 6:
            raise ValueError("The flight number must be 6 characters long.")

        self._flight_number = value

    @property
    def origin(self) -> str:
        return self._origin

    @origin.setter
    def origin(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"The type of {value} is not str.")

        if not value.strip():
            raise ValueError("The origin can not be empty.")

        if len(value.strip()) != 3:
            raise ValueError("The origin must be 3 characters long.")

        self._origin = value

    @property
    def destination(self) -> str:
        return self._destination

    @destination.setter
    def destination(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"The type of {value} is not str.")

        if not value.strip():
            raise ValueError("The destination can not be empty.")

        if len(value.strip()) != 3:
            raise ValueError("The origin must be 3 characters long.")

        self._destination = value

    @property
    def distance_km(self) -> int:
        return self._distance_km

    @distance_km.setter
    def distance_km(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"The type of {value} is not int.")

        if value <= 0:
            raise ValueError("The distance km can not be negative or zero.")

        self._distance_km = value

    @property
    def duration_min(self) -> int:
        return self._duration_min

    @duration_min.setter
    def duration_min(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"The type of {value} is not int.")

        if value <= 0:
            raise ValueError("The duration min can not be negative or zero.")

        self._duration_min = value
