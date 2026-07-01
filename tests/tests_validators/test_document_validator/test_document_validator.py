import pytest

from src.common.exceptions import DuplicatedDocument
from src.core.validators import DocumentValidator
from src.entities import Document

def test_document_validator_no_exception(document_validator: DocumentValidator, document_requested: Document) -> None:
    document_validator.check_existence([document_requested.identity_key], [])

def test_document_validator_duplicated_document(document_validator: DocumentValidator, document_requested: Document) -> None:
    with pytest.raises(DuplicatedDocument):
        document_validator.check_existence([document_requested.identity_key], [document_requested])