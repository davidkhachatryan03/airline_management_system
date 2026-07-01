from uuid import UUID

import pytest

from src.common.exceptions import FullFlight, InexistentFlight, NotScheduledFlight
from src.core.validators import FlightValidator
from src.entities import Flight

def test_flight_validator_no_exception(flight_validator: FlightValidator, flights_requested: list[Flight], flights_id_requested: list[UUID], seats_available_per_flight: dict[UUID, int]) -> None:
    flight_validator.check_flights_existence(flights_id_requested, flights_requested)
    flight_validator.check_flights_statuses(flights_requested)
    
    flight_validator.check_seats_available_per_flight(seats_available_per_flight, 1)

def test_flight_validator_full_flight(flight_validator: FlightValidator, seats_available_per_flight: dict[UUID, int]) -> None:
    with pytest.raises(FullFlight):
        flight_validator.check_seats_available_per_flight(seats_available_per_flight, 10)

def test_flight_validator_inexistent_flight(flight_validator: FlightValidator, flights_id_requested: list[UUID]) -> None:
    with pytest.raises(InexistentFlight):
        flight_validator.check_flights_existence(flights_id_requested, [])
    
def test_flight_validator_not_scheduled_flight(flight_validator: FlightValidator, flights_requested: list[Flight]) -> None:
    flights_requested[0].current_status_id = 99
    with pytest.raises(NotScheduledFlight):
        flight_validator.check_flights_statuses(flights_requested)