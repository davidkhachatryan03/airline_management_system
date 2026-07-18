from datetime import date
from uuid import UUID

import pytest
from pytest_mock import MockerFixture

from src.api.schemas import DocumentRequest
from src.common.types import DocumentId
from src.entities import Passenger


@pytest.fixture
def document_request(passenger_generated: Passenger) -> DocumentRequest:
    return DocumentRequest(
        document_number="ABC123456",
        valid_from=date(2020,1,1),
        valid_until=date(2030,1,1),
        issue_country="ARG",
        passenger_id=passenger_generated.id,
        document_type_id=1
    )

@pytest.fixture
def fixed_document_identifiers(mocker: MockerFixture, expected_document_id: DocumentId) -> None:

    mocker.patch(
        "src.entities.document.uuid6.uuid7",
        return_value=expected_document_id
    )

@pytest.fixture
def passenger_generated() -> Passenger:
    return Passenger.new_passenger(
            full_name="David Khachatryan",
            birth_date=date(2000,1,1),
            email="mail@example.com",
            phone_number="1123456789"
            )

@pytest.fixture
def expected_document_id() -> DocumentId:
    return UUID("12345678-1234-5678-1234-567812345678")