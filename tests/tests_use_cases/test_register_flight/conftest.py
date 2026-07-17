from datetime import datetime
from decimal import Decimal
import pytest
from pytest_mock import MockerFixture
from uuid import UUID

from src.common.types import DocumentId, FlightId
from src.entities import Flight

@pytest.fixture
def flight_generated() -> Flight:
    return Flight.new_flight(
        scheduled_departure_datetime=datetime(2026,1,1),
        scheduled_arrival_datetime=datetime(2026,1,2),
        operating_cost_usd=Decimal("8000"),
        route_id=1,
        airplane_id=1
    )

@pytest.fixture
def fixed_flight_identifiers(mocker: MockerFixture, expected_document_id: DocumentId) -> None:

    mocker.patch(
        "src.entities.flight.uuid6.uuid7",
        return_value=expected_document_id
    )

@pytest.fixture
def expected_flight_id() -> FlightId:
    return UUID("12345678-1234-5678-1234-567812345678")