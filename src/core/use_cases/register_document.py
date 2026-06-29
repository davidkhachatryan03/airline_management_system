from src.core.units_of_work import RegisterDocumentUoW
from src.core.validators import PassengerValidator, DocumentValidator
from src.api.schemas import DocumentRequest, DocumentResponse
from src.entities import Passenger, Document

class RegisterDocument:

    def __init__(self, uow: RegisterDocumentUoW, passenger_validator: PassengerValidator, document_validator: DocumentValidator) -> None:
        self.uow = uow
        self.passenger_validator = passenger_validator
        self.document_validator = document_validator

    def execute(self, document_request: DocumentRequest) -> DocumentResponse:
        with self.uow as uow:
            passenger_retrieved: list[Passenger] = uow.passenger_repository.retrieve_passengers_by_id([document_request.passenger_id])
            self.passenger_validator.check_existence([document_request.passenger_id], passenger_retrieved)

            document_retrieved: list[Document] = uow.document_repository.retrieve_documents([document_request.identity_key])
            self.document_validator.check_existence([document_request.identity_key], document_retrieved)

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