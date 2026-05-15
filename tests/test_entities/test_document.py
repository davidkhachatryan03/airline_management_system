import pytest
from src.entities import DocumentCreated

def test_valid_document(valid_document: dict) -> None:
    document_created = DocumentCreated(**valid_document)

    assert document_created.document_number == valid_document["document_number"]
    assert document_created.valid_from == valid_document["valid_from"]
    assert document_created.valid_until == valid_document["valid_until"]
    assert document_created.issue_country == valid_document["issue_country"]
    assert document_created.passenger_id == valid_document["passenger_id"]
    assert document_created.document_type_id == valid_document["document_type_id"]

@pytest.mark.parametrize("field, value, expected_exception", [
    ("document_number", 123456, TypeError),
    ("document_number", "   ", ValueError),
    ("document_number", "", ValueError),
    ("document_number", "012345678901234567890", ValueError),
    ("valid_from", 123, TypeError),
    ("valid_until", 123, TypeError),
    ("issue_country", 123, TypeError),
    ("issue_country", "   ", ValueError),
    ("issue_country", "", ValueError),
    ("issue_country", "ABCDEF", ValueError),
    ("passenger_id", "123", TypeError),
    ("passenger_id", 0, ValueError),
    ("passenger_id", -100, ValueError),
    ("document_type_id", "123", TypeError),
    ("document_type_id", 0, ValueError),
    ("document_type_id", -100, ValueError),
])

def test_invalid_document(valid_document: dict, field, value, expected_exception) -> None:
    test_data = valid_document.copy()
    test_data[field] = value

    with pytest.raises(expected_exception):
        DocumentCreated(**test_data)