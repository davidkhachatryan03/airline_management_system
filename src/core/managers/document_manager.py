from src.core.repositories import DocumentRepository
from src.core.validators import DocumentValidator

class DocumentManager:

    def __init__(self, document_repository: DocumentRepository, document_validator: DocumentValidator) -> None:
        self.document_repository = document_repository
        self.document_validator = document_validator