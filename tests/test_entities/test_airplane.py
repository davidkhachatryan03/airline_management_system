import pytest
from src.entities import AirplaneCreated
from decimal import Decimal

def test_valid_airplane(valid_airplane: dict) -> None:
    airplane_created = AirplaneCreated(**valid_airplane)

    assert airplane_created.tail_number == valid_airplane["tail_number"]
    assert airplane_created.manufacturer == valid_airplane["manufacturer"]
    assert airplane_created.model == valid_airplane["model"]
    assert airplane_created.capacity == valid_airplane["capacity"]
    assert airplane_created.range_km == valid_airplane["range_km"]
    assert airplane_created.flight_hour_cost_usd == valid_airplane["flight_hour_cost_usd"]
    assert airplane_created.current_status_id == valid_airplane["current_status_id"]

@pytest.mark.parametrize("field, value, expected_exception", [
    ("tail_number", 123, TypeError),
    ("tail_number", "   ", ValueError),
    ("tail_number", "", ValueError),
    ("tail_number", "abcdefghijk", ValueError),
    ("manufacturer", 123, TypeError),
    ("manufacturer", "   ", ValueError),
    ("manufacturer", "", ValueError),
    ("manufacturer", "abcdefghijklmnñopqrstuvwxyzabcdefghijklmnñopqrstuvwxyzabcdefghijklmnñopqrstuvwxyz", ValueError),
    ("model", 123, TypeError),
    ("model", "   ", ValueError),
    ("model", "", ValueError),
    ("model", "abcdefghijklmnñopqrstuvwxyzabcdefghijklmnñopqrstuvwxyzabcdefghijklmnñopqrstuvwxyz", ValueError),
    ("capacity", "123", TypeError),
    ("capacity", 0, ValueError),
    ("capacity", -100, ValueError),
    ("range_km", "123", TypeError),
    ("range_km", 0, ValueError),
    ("range_km", -100, ValueError),
    ("flight_hour_cost_usd", "123", TypeError),
    ("flight_hour_cost_usd", Decimal("0"), ValueError),
    ("flight_hour_cost_usd", Decimal("-100"), ValueError),
    ("current_status_id", "123", TypeError),
    ("current_status_id", 0, ValueError),
    ("current_status_id", -100, ValueError),
])

def test_invalid_airplane(valid_airplane: dict, field, value, expected_exception) -> None:
    test_data = valid_airplane.copy()
    test_data[field] = value

    with pytest.raises(expected_exception):
        AirplaneCreated(**test_data)