from datetime import datetime
from decimal import Decimal
from fastapi.testclient import TestClient
import pytest

from src.api.main import app
from src.api.routers.create_booking_router import get_booking_creator
from src.api.schemas import BookingResponse
from src.common.exceptions import *

client = TestClient(app)

def test_read_main() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "The server is working."}

def test_create_booking_api_valid_input_and_output(mocker, booking_request: dict) -> None:
    mocker_use_case = mocker.Mock()

    mocker_use_case.execute.return_value = BookingResponse(
        booking_reference="ABC123",
        tickets=["01234567890123", "01234567890123"],
        booking_datetime=datetime(2026,1,1,0,0),
        paid_amount_usd=Decimal("10000")
    )

    app.dependency_overrides[get_booking_creator] = lambda: mocker_use_case

    response = client.post("/api/bookings", json=booking_request)
    response_data = response.json()

    app.dependency_overrides.clear()

    assert len(response_data) == 4
    assert response.status_code == 200
    assert response_data["booking_reference"] == "ABC123"
    assert response_data["tickets"] == ["01234567890123", "01234567890123"]
    assert response_data["booking_datetime"] == "2026-01-01T00:00:00"
    assert response_data["paid_amount_usd"] == "10000"

@pytest.mark.parametrize("expected_exception, status_code", [
    (InexistentFlight, 404),
    (BlacklistedPassenger, 403),
    (FullFlight, 409),
    (NotScheduledFlight, 400),
    (InvalidData, 400)
])

def test_create_booking_api_invalid_input(mocker, booking_request: dict, expected_exception, status_code) -> None:
    mocker_use_case = mocker.Mock()

    mocker_use_case.execute.side_effect = expected_exception

    app.dependency_overrides[get_booking_creator] = lambda: mocker_use_case

    response = client.post("/api/bookings", json=booking_request)
    response_data = response.json()

    app.dependency_overrides.clear()

    assert len(response_data) == 2
    assert response.status_code == status_code
    assert response_data["error"] == expected_exception.__name__
    assert response_data["message"] == str(expected_exception())
