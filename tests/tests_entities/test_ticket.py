import pytest
from decimal import Decimal
from uuid import UUID

from src.entities import Ticket

def test_ticket_valid_input(ticket: Ticket) -> None:

    assert ticket.id == UUID("019e92b3-e0db-7244-a9a2-43322a076e75")
    assert ticket.ticket_number == "1234567890123"
    assert ticket.paid_amount_usd == Decimal("13000")
    assert ticket.current_status_id == 1
    assert ticket.booking_id == UUID("019e97c2-2c47-70a5-a87d-a04de3b9c11f")
    assert ticket.flight_id == UUID("019e97c2-2c47-73ad-8730-18e7d13cfbf7")
    assert ticket.passenger_id == UUID("019e97c2-2c47-73ad-8730-18e7d13cfbf7")

def test_new_booking_classmethod_valid_input(ticket: Ticket) -> None:
    new_ticket = Ticket.new_ticket(
        paid_amount_usd=ticket.paid_amount_usd,
        booking_id=ticket.booking_id,
        flight_id=ticket.flight_id,
        passenger_id=ticket.passenger_id
    )

    assert isinstance (new_ticket.id, UUID)
    assert isinstance (new_ticket.ticket_number, str)
    assert new_ticket.paid_amount_usd == ticket.paid_amount_usd
    assert new_ticket.current_status_id == 1
    assert new_ticket.booking_id == ticket.booking_id
    assert new_ticket.flight_id == ticket.flight_id
    assert new_ticket.passenger_id == ticket.passenger_id

@pytest.mark.parametrize(
    "field, value, exception, message", [
        ("id", 123, TypeError, "The type of the id is not UUID."),
        ("ticket_number", 123, TypeError, "The type of the ticket number is not str."),
        ("ticket_number", "   ", ValueError, "The ticket number can not be empty."),
        ("ticket_number", "123", ValueError, "The ticket number must be exactly 13 characters long."),
        ("ticket_number", "".join(["1"] * 14), ValueError, "The ticket number must be exactly 13 characters long."),
        ("ticket_number", "ABC1234567890", ValueError, "The ticket number must only contain digits."),
        ("paid_amount_usd", 123, TypeError, "The type of the paid amount is not decimal."),
        ("paid_amount_usd", Decimal("0"), ValueError, "The paid amount can not be negative or zero."),
        ("paid_amount_usd", Decimal("-10"), ValueError, "The paid amount can not be negative or zero."),
        ("current_status_id", "1", TypeError, "The type of the current status id is not int."),
        ("current_status_id", 0, ValueError, "The current status id can not be negative or zero."),
        ("current_status_id", -10, ValueError, "The current status id can not be negative or zero."),
        ("booking_id", 123, TypeError, "The type of the booking id is not UUID."),
        ("flight_id", 123, TypeError, "The type of the flight id is not UUID."),
        ("passenger_id", 123, TypeError, "The type of the passenger id is not UUID."),
    ]
)

def test_invalid_ticket(ticket: Ticket, field, value, exception, message) -> None:
    test_data: dict = ticket.to_dict()
    test_data[field] = value

    with pytest.raises(exception, match=message):
        Ticket(**test_data)