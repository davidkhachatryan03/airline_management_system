import pytest
from src.entities import TicketCreated
from decimal import Decimal

def test_valid_ticket(valid_ticket: dict) -> None:
    ticket_created = TicketCreated(**valid_ticket)

    assert ticket_created.ticket_number == valid_ticket["ticket_number"]
    assert ticket_created.paid_amount_usd == valid_ticket["paid_amount_usd"]
    assert ticket_created.current_status_id == valid_ticket["current_status_id"]
    assert ticket_created.booking_id == valid_ticket["booking_id"]
    assert ticket_created.passenger_id == valid_ticket["passenger_id"]

@pytest.mark.parametrize("field, value, expected_exception", [
    ("ticket_number", 123, TypeError),
    ("ticket_number", "   ", ValueError),
    ("ticket_number", "", ValueError),
    ("ticket_number", "123", ValueError),
    ("ticket_number", "123456789012A", ValueError),
    ("paid_amount_usd", "123", TypeError),
    ("paid_amount_usd", Decimal("0"), ValueError),
    ("paid_amount_usd", Decimal("-100"), ValueError),
    ("current_status_id", "123", TypeError),
    ("current_status_id", 0, ValueError),
    ("current_status_id", -100, ValueError),
    ("booking_id", "123", TypeError),
    ("booking_id", 0, ValueError),
    ("booking_id", -100, ValueError),
    ("passenger_id", "123", TypeError),
    ("passenger_id", 0, ValueError),
    ("passenger_id", -100, ValueError),
])

def test_invalid_ticket(valid_ticket: dict, field: str, value, expected_exception) -> None:
    test_data = valid_ticket.copy()
    test_data[field] = value

    with pytest.raises(expected_exception):
        TicketCreated(**test_data)