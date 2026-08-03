from datetime import datetime, timedelta

import pytest
import uuid6
from pydantic import ValidationError

from src.api.schemas import FlightRequest, FlightResponse


def test_flight_request_valid_data() -> None:
    departure = datetime(2026, 8, 1, 10, 0, 0)
    arrival = datetime(2026, 8, 1, 14, 0, 0)

    data = {
        "scheduled_departure_datetime": departure,
        "scheduled_arrival_datetime": arrival,
        "route_id": 105,
        "airplane_id": 22,
    }

    request = FlightRequest(**data)

    assert request.route_id == 105
    assert request.airplane_id == 22

    assert request.identity_key == (departure, 105)


def test_flight_request_invalid_route_id_raises_error() -> None:
    data = {
        "scheduled_departure_datetime": datetime.now(),
        "scheduled_arrival_datetime": datetime.now() + timedelta(hours=2),
        "route_id": 0,
        "airplane_id": 22,
    }

    with pytest.raises(ValidationError) as exc_info:
        FlightRequest(**data)

    error_msg = str(exc_info.value)
    assert "route_id" in error_msg
    assert "Input should be greater than 0" in error_msg


def test_flight_request_invalid_airplane_id_raises_error() -> None:
    data = {
        "scheduled_departure_datetime": datetime.now(),
        "scheduled_arrival_datetime": datetime.now() + timedelta(hours=2),
        "route_id": 105,
        "airplane_id": -5,
    }

    with pytest.raises(ValidationError) as exc_info:
        FlightRequest(**data)

    error_msg = str(exc_info.value)
    assert "airplane_id" in error_msg
    assert "Input should be greater than 0" in error_msg


def test_flight_response_valid_data() -> None:
    flight_id = uuid6.uuid7()
    data = {"id": flight_id}

    response = FlightResponse(**data)
    assert response.id == flight_id


def test_flight_response_invalid_uuid_raises_error() -> None:
    data = {"id": "un-string-que-no-es-uuid"}

    with pytest.raises(ValidationError) as exc_info:
        FlightResponse(**data)

    assert "Input should be a valid UUID" in str(exc_info.value)
