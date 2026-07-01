from datetime import date
from uuid import UUID

import pytest

from src.core.validators import DocumentValidator
from src.entities import Document

@pytest.fixture
def document_validator() -> DocumentValidator:
    return DocumentValidator()

@pytest.fixture
def document_requested() -> Document:
    return Document.new_document(
        document_number="AA123456",
        valid_from=date(2020,1,1),
        valid_until=date(2030,1,1),
        issue_country="ARG",
        passenger_id=UUID("019f1de8-e30d-7e0f-9ca0-ea54e0fa4935"),
        document_type_id=1
    )