from uuid import UUID

from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from src.api.main import app
from src.api.routers.flight_router import create_register_flight
from src.api.schemas import FlightRequest, FlightResponse
from src.common.exceptions import (
    InexistentAirplane,
    InexistentRoute,
    MultipleExceptionsError,
)


def test_flight_router_no_exceptions(
    mocker: MockerFixture,
    client: TestClient,
    flight_request: FlightRequest,
    flight_response: FlightResponse,
) -> None:
    mock_use_case = mocker.Mock()
    mock_use_case.execute.return_value = flight_response

    app.dependency_overrides[create_register_flight] = lambda: mock_use_case

    response = client.post("/api/flights", json=flight_request.model_dump(mode="json"))

    assert response.status_code == 200
    assert response.json() == flight_response.model_dump(mode="json")


def test_flight_router_multiple_exceptions(
    mocker: MockerFixture, client: TestClient, flight_request: FlightRequest
) -> None:
    mock_use_case = mocker.Mock()
    mock_use_case.execute.side_effect = MultipleExceptionsError(
        [InexistentAirplane(id=flight_request.airplane_id), InexistentRoute(id=1)]
    )

    app.dependency_overrides[create_register_flight] = lambda: mock_use_case

    response = client.post("/api/flights", json=flight_request.model_dump(mode="json"))

    expected_response = {
        "total_errors": 2,
        "details": [
            {
                "error": "InexistentAirplane",
                "message": f"The airplane with id {flight_request.airplane_id} is not registered.",
                "internal_code": 404,
            },
            {
                "error": "InexistentRoute",
                "message": "The route with id 1 is not registered.",
                "internal_code": 404,
            },
        ],
    }

    assert response.status_code == 422
    assert response.json() == expected_response
