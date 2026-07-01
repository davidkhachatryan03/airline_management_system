from datetime import date
from decimal import Decimal
import pytest
from uuid6 import uuid7

from src.common import DBManager
from src.core.repositories import DocumentRepository
from src.entities import Document

@pytest.fixture
def document_repository(db_connected: DBManager) -> DocumentRepository:
    return DocumentRepository(db_connected)

def get_document() -> Document:
    return Document.new_document(
        document_number="AA123456",
        valid_from=date(2020,1,1),
        valid_until=date(2030,1,1),
        issue_country="ARG",
        passenger_id=uuid7(),
        document_type_id=1
    )

@pytest.fixture
def document() -> Document:
    return get_document()

@pytest.fixture
def documents(cant: int = 1) -> list[Document]:
    return [get_document() for _ in range(cant)]