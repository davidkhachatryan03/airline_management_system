from decimal import Decimal
from uuid import UUID

import pytest
from uuid6 import uuid7

from src.entities import Ticket


@pytest.fixture
def data():
    return {
        "id": uuid7(),
        "ticket_number": "1234567890123",
        "paid_amount_usd": Decimal("13000"),
        "current_status_id": 1,
        "booking_id": uuid7(),
        "flight_id": uuid7(),
        "passenger_id": uuid7(),
    }


def test_ticket_valid_input(data) -> None:
    ticket = Ticket(**data)

    assert ticket.to_dict() == data


def test_new_booking_classmethod_valid_input(mocker, data) -> None:
    mocker.patch("src.entities.ticket.uuid7", return_value=data["id"])

    ticket = Ticket.new_ticket(
        paid_amount_usd=data["paid_amount_usd"],
        booking_id=data["booking_id"],
        flight_id=data["flight_id"],
        passenger_id=data["passenger_id"],
    )

    assert ticket.id == data["id"]
    assert len(ticket.ticket_number) == 13
    assert ticket.ticket_number.isnumeric()
    assert ticket.paid_amount_usd == ticket.paid_amount_usd
    assert ticket.current_status_id == 1
    assert ticket.booking_id == ticket.booking_id
    assert ticket.flight_id == ticket.flight_id
    assert ticket.passenger_id == ticket.passenger_id


@pytest.mark.parametrize(
    "field, value, exception, message",
    [
        ("id", 123, TypeError, "The type of the id is not UUID."),
        ("ticket_number", 123, TypeError, "The type of the ticket number is not str."),
        ("ticket_number", "   ", ValueError, "The ticket number can not be empty."),
        (
            "ticket_number",
            "123",
            ValueError,
            "The ticket number must be exactly 13 characters long.",
        ),
        (
            "ticket_number",
            "".join(["1"] * 14),
            ValueError,
            "The ticket number must be exactly 13 characters long.",
        ),
        (
            "ticket_number",
            "ABC1234567890",
            ValueError,
            "The ticket number must only contain digits.",
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
        ("booking_id", 123, TypeError, "The type of the booking id is not UUID."),
        ("flight_id", 123, TypeError, "The type of the flight id is not UUID."),
        ("passenger_id", 123, TypeError, "The type of the passenger id is not UUID."),
    ],
)
def test_invalid_ticket(data, field, value, exception, message) -> None:
    data[field] = value

    with pytest.raises(exception, match=message):
        Ticket(**data)
