from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

import pytest

from src.entities import Airplane, Booking, Document, Flight, Passenger, Ticket


@pytest.fixture
def airplane() -> Airplane:
    return Airplane(
        id=10,
        tail_number="ABC-123",
        manufacturer="Airbus",
        model="123-200",
        capacity=132,
        range_km=6749,
        flight_hour_cost_usd=Decimal("2000"),
        current_status_id=1,
    )


@pytest.fixture
def booking() -> Booking:
    return Booking(
        id=UUID("019e92b3-e0db-7244-a9a2-43322a076e75"),
        booking_reference="ABC123",
        booking_datetime=datetime(2026, 1, 1),
        paid_amount_usd=Decimal("10000.76"),
        current_status_id=1,
    )


@pytest.fixture
def flight() -> Flight:
    return Flight(
        id=UUID("019e92b3-e0db-7244-a9a2-43322a076e75"),
        scheduled_departure_datetime=datetime(2026, 1, 1),
        scheduled_arrival_datetime=datetime(2026, 1, 2),
        actual_departure_datetime=datetime(2026, 1, 1),
        actual_arrival_datetime=datetime(2026, 1, 2),
        operating_cost_usd=Decimal("10000"),
        base_price_usd=Decimal("13000"),
        current_status_id=1,
        route_id=1,
        airplane_id=1,
    )


@pytest.fixture
def ticket() -> Ticket:
    return Ticket(
        id=UUID("019e92b3-e0db-7244-a9a2-43322a076e75"),
        ticket_number="1234567890123",
        paid_amount_usd=Decimal("13000"),
        current_status_id=1,
        booking_id=UUID("019e97c2-2c47-70a5-a87d-a04de3b9c11f"),
        flight_id=UUID("019e97c2-2c47-73ad-8730-18e7d13cfbf7"),
        passenger_id=UUID("019e97c2-2c47-73ad-8730-18e7d13cfbf7"),
    )


@pytest.fixture
def passenger() -> Passenger:
    return Passenger(
        id=UUID("019e92b3-e0db-7244-a9a2-43322a076e75"),
        full_name="David Khachatryan",
        birth_date=date(2000, 1, 1),
        email="dkh@email.com",
        phone_number="12345678",
        is_blacklisted=False,
        is_vip=True,
    )


@pytest.fixture
def document() -> Document:
    return Document(
        id=UUID("019e92b3-e0db-7244-a9a2-43322a076e75"),
        document_number="AB12345678",
        valid_from=date(2024, 1, 1),
        valid_until=date(2034, 1, 1),
        issue_country="ARG",
        passenger_id=UUID("019e97c2-2c47-73ad-8730-18e7d13cfbf7"),
        document_type_id=1,
    )
