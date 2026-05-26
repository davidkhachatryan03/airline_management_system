from src.core.repositories import DocumentRepository

class DocumentValidator:

    def __init__(self, document_repository: DocumentRepository) -> None:
        self.document_repository = document_repository