from typing import cast
from uuid import UUID

import pytest

from src.api.schemas import DocumentRequest, DocumentResponse
from src.common.exceptions import (
    DuplicatedDocument,
    InexistentPassenger,
    MultipleExceptionsError,
)
from src.core.units_of_work import RegisterDocumentUoW
from src.core.use_cases import (
    RegisterDocument,
    RegisterDocumentValidator,
)
from src.core.validators import BaseValidator
from src.entities import Document, Passenger
from tests.factories import (
    DocumentFactory,
    PassengerFactory,
)
from tests.fakes.fake_db_manager import FakeDBManager
from tests.fakes.fake_uows.fake_register_document_uow import FakeRegisterDocumentUoW


def create_register_document(fake_uow: FakeRegisterDocumentUoW) -> RegisterDocument:
    return RegisterDocument(
        uow=cast(RegisterDocumentUoW, fake_uow),
        register_document_validator=RegisterDocumentValidator(
            base_validator=BaseValidator()
        ),
    )


def test_register_document_valid_input() -> None:
    uow = FakeRegisterDocumentUoW(FakeDBManager())

    passenger: Passenger = PassengerFactory()
    document: Document = DocumentFactory()
    document_request = DocumentRequest(
        document_number=document.document_number,
        valid_from=document.valid_from,
        valid_until=document.valid_until,
        issue_country=document.issue_country,
        passenger_id=passenger.id,
        document_type_id=document.document_type_id,
    )

    uow.passenger_repository.insert([passenger])

    register_document: RegisterDocument = create_register_document(uow)

    document_response: DocumentResponse = register_document.execute(document_request)

    document_retrieved: Document = list(uow.document_repository.storage.values())[0]

    assert document_response.document_number == document_retrieved.document_number
    assert document_response.document_type_id == document_retrieved.document_type_id

    assert isinstance(document_retrieved.id, UUID)
    assert uow.document_repository.storage == {
        document_retrieved.id: document_retrieved
    }


def test_register_document_inexistent_passenger() -> None:
    uow = FakeRegisterDocumentUoW(FakeDBManager())

    passenger: Passenger = PassengerFactory()
    document: Document = DocumentFactory()
    document_request = DocumentRequest(
        document_number=document.document_number,
        valid_from=document.valid_from,
        valid_until=document.valid_until,
        issue_country=document.issue_country,
        passenger_id=passenger.id,
        document_type_id=document.document_type_id,
    )

    register_document: RegisterDocument = create_register_document(uow)

    with pytest.raises(MultipleExceptionsError) as exc:
        register_document.execute(document_request)

    exceptions = {str(exception) for exception in exc.value.exceptions}

    assert exceptions == {str(InexistentPassenger(passenger.id))}


def test_register_document_duplicated_document() -> None:
    uow = FakeRegisterDocumentUoW(FakeDBManager())

    passenger: Passenger = PassengerFactory()
    document: Document = DocumentFactory()
    document_request = DocumentRequest(
        document_number=document.document_number,
        valid_from=document.valid_from,
        valid_until=document.valid_until,
        issue_country=document.issue_country,
        passenger_id=passenger.id,
        document_type_id=document.document_type_id,
    )

    uow.passenger_repository.insert([passenger])
    uow.document_repository.insert([document])

    register_document: RegisterDocument = create_register_document(uow)

    with pytest.raises(MultipleExceptionsError) as exc:
        register_document.execute(document_request)

    exceptions = {str(exception) for exception in exc.value.exceptions}

    assert exceptions == {str(DuplicatedDocument(document.identity_key))}
