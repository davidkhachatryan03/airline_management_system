from datetime import datetime
from decimal import Decimal
import pytest
from uuid import UUID

from src.entities import Flight

def test_flight_completed_valid_input(flight: Flight) -> None:

    assert flight.id == UUID("019e92b3-e0db-7244-a9a2-43322a076e75")
    assert flight.scheduled_departure_datetime == datetime(2026, 1, 1)
    assert flight.scheduled_arrival_datetime == datetime(2026, 1, 2)
    assert flight.actual_departure_datetime == datetime(2026, 1, 1)
    assert flight.actual_arrival_datetime == datetime(2026, 1, 2)
    assert flight.operating_cost_usd == Decimal("10000")
    assert flight.base_price_usd == Decimal("13000")
    assert flight.current_status_id == 1
    assert flight.route_id == 1
    assert flight.airplane_id == 1

def test_flight_uncompleted_valid_input(flight: Flight) -> None:
    flight.actual_departure_datetime = None
    flight.actual_arrival_datetime = None

    assert flight.id == UUID("019e92b3-e0db-7244-a9a2-43322a076e75")
    assert flight.scheduled_departure_datetime == datetime(2026, 1, 1)
    assert flight.scheduled_arrival_datetime == datetime(2026, 1, 2)
    assert flight.actual_departure_datetime == None
    assert flight.actual_arrival_datetime == None
    assert flight.operating_cost_usd == Decimal("10000")
    assert flight.base_price_usd == Decimal("13000")
    assert flight.current_status_id == 1
    assert flight.route_id == 1
    assert flight.airplane_id == 1

def test_new_flight_classmethod_valid_input(flight: Flight) -> None:
    new_flight = Flight.new_flight(
        scheduled_departure_datetime=flight.scheduled_departure_datetime,
        scheduled_arrival_datetime=flight.scheduled_arrival_datetime,
        operating_cost_usd=flight.operating_cost_usd,
        route_id=flight.route_id,
        airplane_id=flight.airplane_id
    )

    assert isinstance(new_flight.id, UUID)
    assert new_flight.scheduled_departure_datetime == flight.scheduled_departure_datetime
    assert new_flight.scheduled_arrival_datetime == flight.scheduled_arrival_datetime
    assert new_flight.actual_departure_datetime == None
    assert new_flight.actual_arrival_datetime == None
    assert new_flight.operating_cost_usd == flight.operating_cost_usd
    assert new_flight.base_price_usd == flight.base_price_usd
    assert new_flight.current_status_id == flight.current_status_id
    assert new_flight.route_id == flight.route_id
    assert new_flight.airplane_id == flight.airplane_id

@pytest.mark.parametrize(
        "field, value, exception, message", [
            ("id", 123, TypeError, "The type of the id is not UUID."),
            ("scheduled_departure_datetime", 123, TypeError, "The type of the scheduled departure datetime must be datetime or none."),
            ("scheduled_arrival_datetime", 123, TypeError, "The type of the scheduled arrival datetime must be datetime or none."),
            ("actual_departure_datetime", 123, TypeError, "The type of the actual departure datetime must be datetime or none."),
            ("actual_arrival_datetime", 123, TypeError, "The type of the actual arrival datetime must be datetime or none."),
            ("operating_cost_usd", Decimal("0"), ValueError, "The operating cost can not be negative or zero."),
            ("operating_cost_usd", Decimal("-10"), ValueError, "The operating cost can not be negative or zero."),
            ("base_price_usd", Decimal("0"), ValueError, "The base price can not be negative or zero."),
            ("base_price_usd", Decimal("-10"), ValueError, "The base price can not be negative or zero."),
            ("current_status_id", "1", TypeError, "The type of the current status id is not int."),
            ("current_status_id", 0, ValueError, "The current status id can not be negative or zero."),
            ("current_status_id", -10, ValueError, "The current status id can not be negative or zero."),
            ("route_id", "1", TypeError, "The type of the route id is not int."),
            ("route_id", 0, ValueError, "The route id can not be negative or zero."),
            ("route_id", -10, ValueError, "The route id can not be negative or zero."),
            ("airplane_id", "1", TypeError, "The type of the airplane id is not int."),
            ("airplane_id", 0, ValueError, "The airplane id can not be negative or zero."),
            ("airplane_id", -10, ValueError, "The airplane id can not be negative or zero."),
                ]
)

def test_invalid_flight(flight: Flight, field, value, exception, message) -> None:
    test_data: dict = flight.to_dict()
    test_data[field] = value

    with pytest.raises(exception, match=message):
        Flight(**test_data)