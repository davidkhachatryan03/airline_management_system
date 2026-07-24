from uuid import UUID

from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from src.api.main import app
from src.api.routers.booking_router import create_register_booking
from src.api.schemas import BookingRequest, BookingResponse
from src.common.exceptions import (FullFlight, InexistentFlight,
                                MultipleExceptionsError, NotScheduledFlight)


def test_booking_router_no_exceptions(
    mocker: MockerFixture,
    client: TestClient,
    booking_request: BookingRequest,
    booking_response: BookingResponse,
) -> None:
    mock_use_case = mocker.Mock()
    mock_use_case.execute.return_value = booking_response

    app.dependency_overrides[create_register_booking] = lambda: mock_use_case

    response = client.post(
        "/api/bookings", json=booking_request.model_dump(mode="json")
    )

    assert response.status_code == 200
    assert response.json() == booking_response.model_dump(mode="json")


def test_booking_router_multiple_exceptions(
    mocker: MockerFixture, client: TestClient, booking_request: BookingRequest
) -> None:
    mock_use_case = mocker.Mock()
    mock_use_case.execute.side_effect = MultipleExceptionsError(
        [
            InexistentFlight(id=UUID("019f75c1-ab3f-7a29-a624-9da6c04e5a70")),
            FullFlight(id=UUID("019f75c2-0bc0-7621-8076-938557f90534")),
            NotScheduledFlight(id=UUID("019f75c2-5470-7d11-a126-2a11c28ae39b")),
        ]
    )

    app.dependency_overrides[create_register_booking] = lambda: mock_use_case

    response = client.post(
        "/api/bookings", json=booking_request.model_dump(mode="json")
    )

    expected_response = {
        "total_errors": 3,
        "details": [
            {
                "error": "InexistentFlight",
                "message": "The flight with id 019f75c1-ab3f-7a29-a624-9da6c04e5a70 is not registered.",
                "internal_code": 404,
            },
            {
                "error": "FullFlight",
                "message": "The flight with id 019f75c2-0bc0-7621-8076-938557f90534 is full.",
                "internal_code": 409,
            },
            {
                "error": "NotScheduledFlight",
                "message": "The flight with id 019f75c2-5470-7d11-a126-2a11c28ae39b is not scheduled.",
                "internal_code": 409,
            },
        ],
    }

    assert response.status_code == 422
    assert response.json() == expected_response
