from collections.abc import Sequence
from typing import cast

import pytest

from src.api.schemas import DocumentRequest, DocumentResponse
from src.common.exceptions import (DuplicatedDocument, InexistentPassenger,
                                    InvalidData, MultipleExceptionsError)
from src.core.units_of_work import RegisterDocumentUoW
from src.core.use_cases import RegisterDocument, RegisterDocumentValidator
from src.core.validators import BaseValidator
from src.entities import Document, Passenger
from tests.fakes.fake_db_manager import FakeDBManager
from tests.fakes.fake_uows.fake_register_document_uow import \
    FakeRegisterDocumentUoW


def create_register_document(fake_uow: FakeRegisterDocumentUoW) -> RegisterDocument:
    return RegisterDocument(
        uow=cast(RegisterDocumentUoW, fake_uow),
        register_document_validator=RegisterDocumentValidator(BaseValidator()),
    )


@pytest.mark.usefixtures("fixed_document_identifiers")
def test_register_document_valid_input(
    document_request: DocumentRequest, passenger_generated: Passenger
) -> None:
    fake_uow = FakeRegisterDocumentUoW(FakeDBManager())

    fake_uow.passenger_repository.insert_passengers([passenger_generated])

    register_document: RegisterDocument = create_register_document(fake_uow)
    document_response: DocumentResponse = register_document.execute(document_request)

    document_expected = Document.new_document(
        document_number=document_request.document_number,
        valid_from=document_request.valid_from,
        valid_until=document_request.valid_until,
        issue_country=document_request.issue_country,
        passenger_id=passenger_generated.id,
        document_type_id=document_request.document_type_id,
    )

    assert len(fake_uow.document_repository.documents)
    assert fake_uow.document_repository.documents == [document_expected]

    assert document_response.document_number == document_expected.document_number
    assert document_response.document_type_id == document_expected.document_type_id


def test_register_document_inexistent_passenger(
    document_request: DocumentRequest,
) -> None:
    fake_uow = FakeRegisterDocumentUoW(FakeDBManager())

    register_document: RegisterDocument = create_register_document(fake_uow)

    with pytest.raises(MultipleExceptionsError) as exc_info:
        register_document.execute(document_request)

    exceptions: Sequence[InvalidData] = exc_info.value.exceptions

    assert len(exceptions) == 1
    assert isinstance(exceptions[0], InexistentPassenger)


def test_register_document_duplicated_document(
    document_request: DocumentRequest, passenger_generated: Passenger
) -> None:
    fake_uow = FakeRegisterDocumentUoW(FakeDBManager())

    fake_uow.passenger_repository.insert_passengers([passenger_generated])

    register_document: RegisterDocument = create_register_document(fake_uow)

    register_document.execute(document_request)

    with pytest.raises(MultipleExceptionsError) as exc_info:
        register_document.execute(document_request)

    exceptions: Sequence[InvalidData] = exc_info.value.exceptions

    assert len(exceptions) == 1
    assert isinstance(exceptions[0], DuplicatedDocument)
