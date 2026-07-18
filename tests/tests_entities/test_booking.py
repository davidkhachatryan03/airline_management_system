from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID

import pytest

from src.entities import Booking, Flight


def test_booking_valid_input(booking: Booking) -> None:

    assert booking.id == UUID("019e92b3-e0db-7244-a9a2-43322a076e75")
    assert booking.booking_reference == "ABC123"
    assert booking.booking_datetime == datetime(2026, 1, 1)
    assert booking.paid_amount_usd == Decimal("10000.76")
    assert booking.current_status_id == 1


def test_new_booking_classmethod_valid_input(
    flight: Flight, number_of_passengers=4
) -> None:
    new_booking = Booking.new_booking([flight.base_price_usd], number_of_passengers)

    calculated_paid_amount_usd: Decimal = (
        flight.base_price_usd * number_of_passengers
    ).quantize(Decimal("0.01"), ROUND_HALF_UP)

    assert isinstance(new_booking.id, UUID)
    assert isinstance(new_booking.booking_reference, str)
    assert isinstance(new_booking.booking_datetime, datetime)
    assert new_booking.paid_amount_usd == calculated_paid_amount_usd
    assert new_booking.current_status_id == 1


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
def test_invalid_booking(booking: Booking, field, value, exception, message) -> None:
    test_data: dict = booking.to_dict()
    test_data[field] = value

    with pytest.raises(exception, match=message):
        Booking(**test_data)
