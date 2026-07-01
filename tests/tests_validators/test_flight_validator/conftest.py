from datetime import datetime
from decimal import Decimal
from uuid import UUID

import pytest

from src.common.exceptions import FullFlight, InexistentFlight, NotScheduledFlight
from src.core.validators import FlightValidator
from src.entities import Flight

@pytest.fixture
def flights_requested() -> list[Flight]:
    flights: list[Flight] = []

    flight_one = Flight.new_flight(
        scheduled_departure_datetime=datetime(2026,1,1,13,24),
        scheduled_arrival_datetime=datetime(2026,1,1,16,46),
        operating_cost_usd=Decimal("13000"),
        route_id=1,
        airplane_id=1
    )

    flight_two = Flight.new_flight(
        scheduled_departure_datetime=datetime(2026,1,7,10,12),
        scheduled_arrival_datetime=datetime(2026,1,7,14,2),
        operating_cost_usd=Decimal("12000"),
        route_id=2,
        airplane_id=1
    )

    flights.extend([flight_one, flight_two])

    return flights

@pytest.fixture
def flights_id_requested(flights_requested: list[Flight]) -> list[UUID]:
    return [flight.id for flight in flights_requested]

@pytest.fixture
def seats_available_per_flight(flights_id_requested: list[UUID]) -> dict[UUID, int]:
    return {id: 1 for id in flights_id_requested}

@pytest.fixture
def flight_validator() -> FlightValidator:
    return FlightValidator()
