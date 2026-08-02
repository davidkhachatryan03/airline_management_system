from decimal import Decimal

import pytest

from src.entities.airplane import Airplane


@pytest.fixture
def data():
    return {
        "id": 10,
        "tail_number": "ABC-123",
        "manufacturer": "Airbus",
        "model": "123-400",
        "capacity": 132,
        "range_km": 6749,
        "flight_hour_cost_usd": Decimal("2000"),
        "current_status_id": 1,
    }


def test_airplane_valid_input(data) -> None:
    airplane = Airplane(**data)

    assert airplane.to_dict() == data


@pytest.mark.parametrize(
    "field, value, exception, message",
    [
        ("id", "1", TypeError, "The type the id is not int."),
        ("id", 0, ValueError, "The id can not be negative or zero."),
        ("id", -5, ValueError, "The id can not be negative or zero."),
        (
            "tail_number",
            123,
            TypeError,
            "The type of 123 is not str.",
        ),
        (
            "tail_number",
            "   ",
            ValueError,
            "The tail number can not be empty.",
        ),
        (
            "tail_number",
            "A" * 11,
            ValueError,
            "The tail number must be 10 characters or less.",
        ),
        (
            "manufacturer",
            123,
            TypeError,
            "The type of 123 is not str.",
        ),
        (
            "manufacturer",
            "   ",
            ValueError,
            "The manufacturer can not be empty.",
        ),
        (
            "manufacturer",
            "A" * 51,
            ValueError,
            "The manufacturer must be 50 characters or less.",
        ),
        (
            "model",
            123,
            TypeError,
            "The type of 123 is not str.",
        ),
        (
            "model",
            "   ",
            ValueError,
            "The model can not be empty.",
        ),
        (
            "model",
            "A" * 51,
            ValueError,
            "The model must be 50 characters or less.",
        ),
        ("capacity", "150", TypeError, "The type of 150 is not int."),
        ("capacity", 0, ValueError, "The capacity can not be negative or zero."),
        ("capacity", -10, ValueError, "The capacity can not be negative or zero."),
        ("range_km", "5000", TypeError, "The type of 5000 is not int."),
        ("range_km", 0, ValueError, "The range can not be negative or zero."),
        ("range_km", -10, ValueError, "The range can not be negative or zero."),
        (
            "flight_hour_cost_usd",
            2500.50,
            TypeError,
            "The type of 2500.5 is not decimal.",
        ),
        (
            "flight_hour_cost_usd",
            Decimal("0.00"),
            ValueError,
            "The flight hour cost can not be negative or zero.",
        ),
        (
            "flight_hour_cost_usd",
            Decimal("-10.00"),
            ValueError,
            "The flight hour cost can not be negative or zero.",
        ),
        ("current_status_id", "1", TypeError, "The type of 1 is not int."),
        (
            "current_status_id",
            0,
            ValueError,
            "The current status id can not be negative or zero.",
        ),
        (
            "current_status_id",
            -10,
            ValueError,
            "The current status id can not be negative or zero.",
        ),
    ],
)
def test_invalid_airplane(data, field, value, exception, message) -> None:
    data[field] = value

    with pytest.raises(exception, match=message):
        Airplane(**data)
