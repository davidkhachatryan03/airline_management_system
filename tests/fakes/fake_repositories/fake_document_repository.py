from src.common.types import DocumentIdentityKey
from src.entities import Document


class FakeDocumentRepository:

    def __init__(self) -> None:
        self.documents: list[Document] = []

    def retrieve_documents_by_identity_key(
        self, documents_requested_identity_keys: list[DocumentIdentityKey]
    ) -> list[Document]:
        documents_retrieved: list[Document] = []
        dict_documents_stored_identity_keys: dict[DocumentIdentityKey, Document] = {document.identity_key: document for document in self.documents}

        for document_requested_identity_key in documents_requested_identity_keys:
            if document_requested_identity_key in dict_documents_stored_identity_keys:
                documents_retrieved.append(dict_documents_stored_identity_keys[document_requested_identity_key])
        
        return documents_retrieved

    def insert_documents(self, documents: list[Document]) -> None:
        self.documents.extend(documents)
