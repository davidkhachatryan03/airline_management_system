from src.entities import Document

class FakeDocumentRepository:

    def __init__(self) -> None:
        self.documents: list[Document] = []

    def retrieve_documents_by_identity_key(self, documents_requested: list[tuple]) -> list[Document]:
        return self.documents
    
    def insert_documents(self, documents: list[Document]) -> None:
        self.documents.extend(documents)