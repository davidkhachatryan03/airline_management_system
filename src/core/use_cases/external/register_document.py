from src.api.schemas import DocumentRequest, DocumentResponse
from src.core.units_of_work import RegisterDocumentUoW
from src.core.validators import BaseValidator
from src.common.exceptions import InexistentPassenger, InvalidData, DuplicatedDocument, MultipleExceptionsError
from src.common.types import PassengerId, DocumentIdentityKey
from src.entities import Document, Passenger

class RegisterDocumentValidator:

    def __init__(self, base_validator: BaseValidator) -> None:
        self.base_validator = base_validator

    def validate_data_logic(self, 
                            passengers_id: list[PassengerId], 
                            passengers_retrieved_id: list[PassengerId]) -> None:
        exceptions: list[InvalidData] = []
        
        passengers_missing_ids: set[PassengerId] = self.base_validator.check_existence(passengers_id, passengers_retrieved_id)

        for passenger_id in passengers_missing_ids:
            exceptions.append(InexistentPassenger(passenger_id))

        if exceptions:
            raise MultipleExceptionsError(exceptions)
    
    def validate_business_logic(self, documents_requested_identity_keys: list[DocumentIdentityKey], documents_retrieved_identity_keys: list[DocumentIdentityKey]) -> None:
        exceptions: list[InvalidData] = []

        documents_missing_identity_keys: set[DocumentIdentityKey] = self.base_validator.check_existence(documents_requested_identity_keys, documents_retrieved_identity_keys)
        
        for document_identity_key in documents_missing_identity_keys:
            exceptions.append(DuplicatedDocument(document_identity_key))
        
        if exceptions:
            raise MultipleExceptionsError(exceptions)

class RegisterDocument:

    def __init__(self, uow: RegisterDocumentUoW, register_document_validator: RegisterDocumentValidator) -> None:
        self.uow = uow
        self.register_document_validator = register_document_validator

    def execute(self, document_request: DocumentRequest) -> DocumentResponse:
        with self.uow as uow:
            passengers_retrieved: list[Passenger] = uow.passenger_repository.retrieve_passengers_by_id([document_request.passenger_id])
            passengers_retrieved_id: list[PassengerId] = [passenger.id for passenger in passengers_retrieved]

            documents_retrieved: list[Document] = uow.document_repository.retrieve_documents_by_identity_key([document_request.identity_key])
            documents_retrieved_identity_keys: list[DocumentIdentityKey] = [document.identity_key for document in documents_retrieved]

            self.register_document_validator.validate_data_logic([document_request.passenger_id], passengers_retrieved_id)
            self.register_document_validator.validate_business_logic([document_request.identity_key], documents_retrieved_identity_keys)

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