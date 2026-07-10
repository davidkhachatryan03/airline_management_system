from src.api.schemas import DocumentRequest, DocumentResponse
from src.core.units_of_work import RegisterDocumentUoW
from src.core.validators import PassengerValidator, DocumentValidator
from src.common.exceptions import InexistentPassenger, DuplicatedDocument
from src.common.types import PassengerId, DocumentIdentityKey
from src.entities import Document, Passenger

class RegisterDocumentValidator:

    def __init__(self, passenger_validator: PassengerValidator, document_validator: DocumentValidator) -> None:
        self.passenger_validator = passenger_validator
        self.document_validator = document_validator

    def validate_data_logic(self, 
                            passengers_id: list[PassengerId], 
                            documents_identity_keys: list[DocumentIdentityKey], 
                            passengers_retrieved: list[Passenger], 
                            documents_retrieved: list[Document]) -> None:
        if not self.passenger_validator.check_existence(passengers_id, passengers_retrieved):
            raise InexistentPassenger

        if self.document_validator.check_existence(documents_identity_keys, documents_retrieved):
            raise DuplicatedDocument

class RegisterDocument:

    def __init__(self, uow: RegisterDocumentUoW, register_document_validator: RegisterDocumentValidator) -> None:
        self.uow = uow
        self.register_document_validator = register_document_validator

    def execute(self, document_request: DocumentRequest) -> DocumentResponse:
        with self.uow as uow:
            passengers_retrieved: list[Passenger] = uow.passenger_repository.retrieve_passengers_by_id([document_request.passenger_id])
            documents_retrieved: list[Document] = uow.document_repository.retrieve_documents_by_identity_key([document_request.identity_key])

            self.register_document_validator.validate_data_logic([document_request.passenger_id], [document_request.identity_key], passengers_retrieved, documents_retrieved)

            document_created = Document.new_document(
                document_number=document_request.document_number,
                valid_from=document_request.valid_from,
                valid_until=document_request.valid_until,
                issue_country=document_request.issue_country,
                passenger_id=document_request.passenger_id,
                document_type_id=document_request.document_type_id
            )
            uow.document_repository.insert_documents([document_created])

            return DocumentResponse(
                document_number=document_created.document_number,
                document_type_id=document_created.document_type_id
            )