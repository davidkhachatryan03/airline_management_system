from datetime import date
import pytest
from typing import cast

from src.api.schemas import DocumentRequest, DocumentResponse
from src.common.exceptions import *
from src.core.use_cases import RegisterDocument
from src.core.units_of_work import RegisterDocumentUoW
from src.core.validators import DocumentValidator, PassengerValidator
from src.entities import Document, Passenger
from tests.fakes.fake_db_manager import FakeDBManager
from tests.fakes.fake_repositories import FakeDocumentRepository, FakePassengerRepository
from tests.fakes.fake_uows.fake_register_document_uow import FakeRegisterDocumentUoW

def make_document_registrar(fake_uow: FakeRegisterDocumentUoW) -> RegisterDocument:
    return RegisterDocument(
        uow=cast(RegisterDocumentUoW, fake_uow),
        passenger_validator=PassengerValidator(),
        document_validator=DocumentValidator()
    )

def test_register_document_use_case_valid_input(document_request: DocumentRequest, passenger_generated: list[Passenger]) -> None:
    fake_uow = FakeRegisterDocumentUoW(FakeDBManager())

    fake_uow.passenger_repository.insert_passengers(passenger_generated)

    assert len(fake_uow.passenger_repository.passengers) == 1
    assert len(fake_uow.document_repository.documents) == 0

    document_registrar: RegisterDocument = make_document_registrar(fake_uow)

    document_response: DocumentResponse = document_registrar.execute(document_request)

    assert len(fake_uow.passenger_repository.passengers) == 1
    assert len(fake_uow.document_repository.documents) == 1

    assert document_response.document_number == document_request.document_number
    assert document_response.document_type_id == document_response.document_type_id

def test_register_document_use_case_invalid_input_duplicated_document(document_request: DocumentRequest, document_generated: list[Document], passenger_generated: list[Passenger]) -> None:
    fake_uow = FakeRegisterDocumentUoW(FakeDBManager())

    fake_uow.passenger_repository.insert_passengers(passenger_generated)
    fake_uow.document_repository.insert_documents(document_generated)

    assert len(fake_uow.passenger_repository.passengers) == 1
    assert len(fake_uow.document_repository.documents) == 1

    document_registrar: RegisterDocument = make_document_registrar(fake_uow)

    with pytest.raises(DuplicatedDocument):
        document_registrar.execute(document_request)

def test_register_document_use_case_invalid_input_inexistent_passenger(document_request: DocumentRequest) -> None:
    fake_uow = FakeRegisterDocumentUoW(FakeDBManager())

    assert len(fake_uow.passenger_repository.passengers) == 0
    assert len(fake_uow.document_repository.documents) == 0

    document_registrar: RegisterDocument = make_document_registrar(fake_uow)

    with pytest.raises(InexistentPassenger):
        document_registrar.execute(document_request)