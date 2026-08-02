from datetime import date
from uuid import UUID

import pytest
from uuid6 import uuid7

from src.entities import Document


@pytest.fixture
def data():
    return {
        "id": uuid7(),
        "document_number": "AB12345678",
        "valid_from": date(2024, 1, 1),
        "valid_until": date(2034, 1, 1),
        "issue_country": "ARG",
        "passenger_id": uuid7(),
        "document_type_id": 1,
    }


def test_document_valid_input(data) -> None:
    document = Document(**data)

    assert document.to_dict() == data


def test_new_document_classmethod_valid_input(mocker, data) -> None:
    mocker.patch("src.entities.document.uuid7", return_value=data["id"])

    document = Document.new_document(
        document_number=data["document_number"],
        valid_from=data["valid_from"],
        valid_until=data["valid_until"],
        issue_country=data["issue_country"],
        passenger_id=data["passenger_id"],
        document_type_id=data["document_type_id"],
    )

    assert document.to_dict() == data


@pytest.mark.parametrize(
    "field, value, exception, message",
    [
        ("id", 123, TypeError, "The type of the id is not UUID."),
        (
            "document_number",
            123,
            TypeError,
            "The type of the document number is not str.",
        ),
        ("document_number", "   ", ValueError, "The document number can not be empty."),
        (
            "document_number",
            "A" * 21,
            ValueError,
            "The document number must be 20 characters or less.",
        ),
        (
            "valid_from",
            "2024-01-01",
            TypeError,
            "The type of the valid from date is not date.",
        ),
        (
            "valid_until",
            "2034-01-01",
            TypeError,
            "The type of the valid until date is not date.",
        ),
        ("issue_country", 123, TypeError, "The type of the issue country is not str."),
        ("issue_country", "   ", ValueError, "The issue country can not be empty."),
        (
            "issue_country",
            "AR",
            ValueError,
            "The issue country must be 3 characters long.",
        ),
        (
            "issue_country",
            "ARGE",
            ValueError,
            "The issue country must be 3 characters long.",
        ),
        ("passenger_id", 123, TypeError, "The type of the passenger id is not UUID."),
        (
            "document_type_id",
            "1",
            TypeError,
            "The type of the document type id is not int.",
        ),
        (
            "document_type_id",
            0,
            ValueError,
            "The document type id can not be negative or zero.",
        ),
        (
            "document_type_id",
            -10,
            ValueError,
            "The document type id can not be negative or zero.",
        ),
    ],
)
def test_invalid_document(data, field, value, exception, message) -> None:
    data[field] = value

    with pytest.raises(exception, match=message):
        Document(**data)
