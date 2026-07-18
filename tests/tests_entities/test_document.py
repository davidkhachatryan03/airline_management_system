from datetime import date
from uuid import UUID

import pytest

from src.entities import Document


def test_document_valid_input(document: Document) -> None:
    assert document.id == UUID("019e92b3-e0db-7244-a9a2-43322a076e75")
    assert document.document_number == "AB12345678"
    assert document.valid_from == date(2024, 1, 1)
    assert document.valid_until == date(2034, 1, 1)
    assert document.issue_country == "ARG"
    assert document.passenger_id == UUID("019e97c2-2c47-73ad-8730-18e7d13cfbf7")
    assert document.document_type_id == 1

def test_new_document_classmethod_valid_input(document: Document) -> None:
    new_doc = Document.new_document(
        document_number=document.document_number,
        valid_from=document.valid_from,
        valid_until=document.valid_until,
        issue_country=document.issue_country,
        passenger_id=document.passenger_id,
        document_type_id=document.document_type_id
    )

    assert isinstance(new_doc.id, UUID)
    assert new_doc.document_number == document.document_number
    assert new_doc.valid_from == document.valid_from
    assert new_doc.valid_until == document.valid_until
    assert new_doc.issue_country == document.issue_country
    assert new_doc.passenger_id == document.passenger_id
    assert new_doc.document_type_id == document.document_type_id

@pytest.mark.parametrize(
    "field, value, exception, message", [
        ("id", 123, TypeError, "The type of the id is not UUID."),
        ("document_number", 123, TypeError, "The type of the document number is not str."),
        ("document_number", "   ", ValueError, "The document number can not be empty."),
        ("document_number", "A" * 21, ValueError, "The document number must be 20 characters or less."),
        ("valid_from", "2024-01-01", TypeError, "The type of the valid from date is not date."),
        ("valid_until", "2034-01-01", TypeError, "The type of the valid until date is not date."),
        ("issue_country", 123, TypeError, "The type of the issue country is not str."),
        ("issue_country", "   ", ValueError, "The issue country can not be empty."),
        ("issue_country", "AR", ValueError, "The issue country must be 3 characters long."),
        ("issue_country", "ARGE", ValueError, "The issue country must be 3 characters long."),
        ("passenger_id", 123, TypeError, "The type of the passenger id is not UUID."),
        ("document_type_id", "1", TypeError, "The type of the document type id is not int."),
        ("document_type_id", 0, ValueError, "The document type id can not be negative or zero."),
        ("document_type_id", -10, ValueError, "The document type id can not be negative or zero."),
    ]
)
def test_invalid_document(document: Document, field, value, exception, message) -> None:
    test_data: dict = document.to_dict()
    test_data[field] = value

    with pytest.raises(exception, match=message):
        Document(**test_data)