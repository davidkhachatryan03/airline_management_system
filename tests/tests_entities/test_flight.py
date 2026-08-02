from datetime import datetime
from decimal import Decimal
from uuid import UUID

import pytest
from uuid6 import uuid7

from src.entities import Flight


@pytest.fixture
def data():
    return {
        "id": uuid7(),
        "scheduled_departure_datetime": datetime(2026, 1, 1),
        "scheduled_arrival_datetime": datetime(2026, 1, 2),
        "actual_departure_datetime": datetime(2026, 1, 1),
        "actual_arrival_datetime": datetime(2026, 1, 2),
        "operating_cost_usd": Decimal("10000"),
        "base_price_usd": Decimal("13000"),
        "current_status_id": 1,
        "route_id": 1,
        "airplane_id": 1,
    }


def test_flight_valid_input(data) -> None:
    flight = Flight(**data)

    assert flight.to_dict() == data


def test_new_flight_classmethod_valid_input(mocker, data) -> None:
    mocker.patch("src.entities.flight.uuid7", return_value=data["id"])

    flight = Flight.new_flight(
        scheduled_departure_datetime=data["scheduled_departure_datetime"],
        scheduled_arrival_datetime=data["scheduled_arrival_datetime"],
        operating_cost_usd=data["operating_cost_usd"],
        route_id=data["route_id"],
        airplane_id=data["airplane_id"],
    )

    data["actual_departure_datetime"] = None
    data["actual_arrival_datetime"] = None

    assert flight.to_dict() == data


@pytest.mark.parametrize(
    "field, value, exception, message",
    [
        ("id", 123, TypeError, "The type of the id is not UUID."),
        (
            "scheduled_departure_datetime",
            123,
            TypeError,
            "The type of the scheduled departure datetime must be datetime or none.",
        ),
        (
            "scheduled_arrival_datetime",
            123,
            TypeError,
            "The type of the scheduled arrival datetime must be datetime or none.",
        ),
        (
            "actual_departure_datetime",
            123,
            TypeError,
            "The type of the actual departure datetime must be datetime or none.",
        ),
        (
            "actual_arrival_datetime",
            123,
            TypeError,
            "The type of the actual arrival datetime must be datetime or none.",
        ),
        (
            "operating_cost_usd",
            Decimal("0"),
            ValueError,
            "The operating cost can not be negative or zero.",
        ),
        (
            "operating_cost_usd",
            Decimal("-10"),
            ValueError,
            "The operating cost can not be negative or zero.",
        ),
        (
            "base_price_usd",
            Decimal("0"),
            ValueError,
            "The base price can not be negative or zero.",
        ),
        (
            "base_price_usd",
            Decimal("-10"),
            ValueError,
            "The base price can not be negative or zero.",
        ),
        (
            "current_status_id",
            "1",
            TypeError,
            "The type of the current status id is not int.",
        ),
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
        ("route_id", "1", TypeError, "The type of the route id is not int."),
        ("route_id", 0, ValueError, "The route id can not be negative or zero."),
        ("route_id", -10, ValueError, "The route id can not be negative or zero."),
        ("airplane_id", "1", TypeError, "The type of the airplane id is not int."),
        ("airplane_id", 0, ValueError, "The airplane id can not be negative or zero."),
        (
            "airplane_id",
            -10,
            ValueError,
            "The airplane id can not be negative or zero.",
        ),
    ],
)
def test_invalid_flight(data, field, value, exception, message) -> None:
    data[field] = value

    with pytest.raises(exception, match=message):
        Flight(**data)
