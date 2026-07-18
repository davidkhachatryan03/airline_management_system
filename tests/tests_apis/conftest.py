from datetime import datetime, date
from decimal import Decimal
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from src.api.main import app
from src.api.schemas import BookingResponse, BookingRequest, DocumentRequest, DocumentResponse, FlightRequest, FlightResponse, PassengerRequest

@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

@pytest.fixture(autouse=True)
def clear_overrides():
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def booking_request() -> BookingRequest:
    return BookingRequest(
        flights_id=[UUID("019f7583-dab6-7c91-b300-dea75404fe5a")],
        passengers=[
            PassengerRequest(
            full_name="David Khachatryan",
            birth_date=date(2000,1,1),
            email="example@mail.com",
            phone_number="123456789",
            document_number="1122334455",
            valid_from=date(2020,1,1),
            valid_until=date(2030,1,1),
            issue_country="ARG",
            document_type_id=1
            )
        ]
    )

@pytest.fixture
def booking_response() -> BookingResponse:
    return BookingResponse(
        booking_reference="ABC123",
        tickets=["1234567890123456"],
        booking_datetime=datetime.now(),
        paid_amount_usd=Decimal("10000")
    )

@pytest.fixture
def document_request() -> DocumentRequest:
    return DocumentRequest(
        document_number="AAA123456",
        valid_from=date(2020,1,1),
        valid_until=date(2030,1,1),
        issue_country="ARG",
        passenger_id=UUID("019f75c6-adeb-7dd7-ae5d-60430c177cc0"),
        document_type_id=1
    )

@pytest.fixture
def document_response(document_request: DocumentRequest) -> DocumentResponse:
    return DocumentResponse(
        document_number=document_request.document_number,
        document_type_id=document_request.document_type_id
    )

@pytest.fixture
def flight_request() -> FlightRequest:
    return FlightRequest(
        scheduled_departure_datetime=datetime(2026,1,1),
        scheduled_arrival_datetime=datetime(2026,1,2),
        route_id=1,
        airplane_id=1
    )

@pytest.fixture
def flight_response() -> FlightResponse:
    return FlightResponse(
        id=UUID("019f75e0-13b6-7346-8ce6-72024cb1ff00")
    )