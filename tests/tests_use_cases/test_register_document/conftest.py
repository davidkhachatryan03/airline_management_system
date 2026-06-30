from datetime import date
import pytest
from uuid import UUID

from src.api.schemas import DocumentRequest, DocumentResponse
from src.entities import Document, Passenger

@pytest.fixture
def document_request() -> DocumentRequest:
    return DocumentRequest(
        document_number="AB123456",
        valid_from=date(2005,1,1),
        valid_until=date(2015,1,1),
        issue_country="ARG",
        passenger_id=UUID("019f18c5-6f30-7b19-8d23-582b3a60bb11"),
        document_type_id=1
    )

@pytest.fixture
def document_generated(document_request: DocumentRequest) -> list[Document]:
    return [Document.new_document(
        document_number=document_request.document_number,
        valid_from=document_request.valid_from,
        valid_until=document_request.valid_until,
        issue_country=document_request.issue_country,
        passenger_id=document_request.passenger_id,
        document_type_id=document_request.document_type_id
    )]

@pytest.fixture
def passenger_generated(document_request: DocumentRequest) -> list[Passenger]:
    passenger = Passenger.new_passenger(
        full_name="David Khachatryan",
        national_identity_number="DD123456",
        issue_country="ARG",
        birth_date=date(2000,1,1),
        email="mail@example.com",
        phone_number="11234567890"
    )

    passenger.id = document_request.passenger_id

    return [passenger]