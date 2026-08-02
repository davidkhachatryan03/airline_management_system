from datetime import datetime
from decimal import Decimal
from uuid import UUID

import pytest
from freezegun import freeze_time
from uuid6 import uuid7

from src.entities import Booking


@pytest.fixture
def data():
    return {
        "id": uuid7(),
        "booking_reference": "ABC123",
        "booking_datetime": datetime(2026, 1, 1),
        "paid_amount_usd": Decimal("10000.76"),
        "current_status_id": 1,
    }


def test_booking_valid_input(data) -> None:
    booking = Booking(**data)

    assert booking.to_dict() == data


@freeze_time("2026-01-01 12:00:00")
def test_new_booking_classmethod_valid_input(mocker, data) -> None:
    mocker.patch("src.entities.booking.uuid7", return_value=data["id"])

    flights_base_prices = [Decimal("1000"), Decimal("2000")]
    number_of_passengers = 4
    booking = Booking.new_booking(
        flights_base_prices=flights_base_prices,
        number_of_passengers=number_of_passengers,
    )

    calculated_paid_amount_usd: Decimal = Decimal("12000")

    assert booking.id == data["id"]
    assert len(booking.booking_reference) == 6
    assert booking.booking_reference.isupper()
    assert booking.booking_reference.isalnum()
    assert booking.booking_datetime == datetime(2026, 1, 1, 12, 0, 0)
    assert booking.paid_amount_usd == calculated_paid_amount_usd
    assert booking.current_status_id == 1


@pytest.mark.parametrize(
    "field, value, exception, message",
    [
        ("id", 123, TypeError, "The type of the id is not UUID."),
        (
            "booking_reference",
            123,
            TypeError,
            "The type of the booking reference is not str.",
        ),
        (
            "booking_reference",
            "   ",
            ValueError,
            "The booking reference can not be empty.",
        ),
        (
            "booking_reference",
            "ABC12",
            ValueError,
            "The booking reference mut be 6 characters long.",
        ),
        (
            "booking_reference",
            "ABC123456",
            ValueError,
            "The booking reference mut be 6 characters long.",
        ),
        (
            "booking_datetime",
            123,
            TypeError,
            "The type of the booking datetime is not datetime.",
        ),
        (
            "paid_amount_usd",
            123,
            TypeError,
            "The type of the paid amount is not decimal.",
        ),
        (
            "paid_amount_usd",
            Decimal("0"),
            ValueError,
            "The paid amount can not be negative or zero.",
        ),
        (
            "paid_amount_usd",
            Decimal("-10"),
            ValueError,
            "The paid amount can not be negative or zero.",
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
    ],
)
def test_invalid_booking(data, field, value, exception, message) -> None:
    data[field] = value

    with pytest.raises(exception, match=message):
        Booking(**data)
