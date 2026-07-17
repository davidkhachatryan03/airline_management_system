from datetime import datetime
from decimal import Decimal
import pytest
from pytest_mock import MockerFixture
from uuid import UUID

from src.api.schemas import FlightRequest
from src.common.types import DocumentId, FlightId
from src.entities import Airplane, Flight, Route

@pytest.fixture
def flight_request(route_generated: Route, airplane_generated: Airplane) -> FlightRequest:
    return FlightRequest(
        scheduled_departure_datetime=datetime(2026,1,1),
        scheduled_arrival_datetime=datetime(2026,1,2),
        route_id=route_generated.id,
        airplane_id=airplane_generated.id
    )

@pytest.fixture
def flight_generated(flight_request: FlightRequest, airplane_generated: Airplane, route_generated: Route) -> Flight:
    return Flight.new_flight(
        scheduled_departure_datetime=flight_request.scheduled_departure_datetime,
        scheduled_arrival_datetime=flight_request.scheduled_arrival_datetime,
        operating_cost_usd=Flight._calculate_operating_cost_usd(airplane_generated.flight_hour_cost_usd, route_generated.duration_min),
        route_id=flight_request.route_id,
        airplane_id=flight_request.airplane_id
    )

@pytest.fixture
def fixed_flight_identifiers(mocker: MockerFixture, expected_flight_id: DocumentId) -> None:

    mocker.patch(
        "src.entities.flight.uuid6.uuid7",
        return_value=expected_flight_id
    )

@pytest.fixture
def expected_flight_id() -> FlightId:
    return UUID("12345678-1234-5678-1234-567812345678")

@pytest.fixture
def route_generated() -> Route:
    return Route(
        id=1,
        flight_number="ABC123",
        origin="EZE",
        destination="MQP",
        distance_km=500,
        duration_min=75
    )

@pytest.fixture
def airplane_generated() -> Airplane:
    return Airplane(
        id=1,
        tail_number="AA-1234",
        manufacturer="Airbus",
        model="A123",
        capacity=120,
        range_km=8000,
        flight_hour_cost_usd=Decimal("1400"),
        current_status_id=1
    )

@pytest.fixture
def unavailable_airplane() -> Airplane:
    return Airplane(
        id=2,
        tail_number="AA-1234",
        manufacturer="Airbus",
        model="A123",
        capacity=120,
        range_km=10,
        flight_hour_cost_usd=Decimal("1400"),
        current_status_id=1
    )