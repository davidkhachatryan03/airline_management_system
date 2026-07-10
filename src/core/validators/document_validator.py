from src.common.types import DocumentIdentityKey
from src.entities import Document

class DocumentValidator:

    def check_existence(self, documents_requested: list[DocumentIdentityKey], documents_retrieved: list[Document]) -> bool:
        requested_ids = set(documents_requested)
        retrieved_ids = {document.identity_key for document in documents_retrieved}
        
        missing_ids = requested_ids - retrieved_ids
        
        if missing_ids:
            return False
            
        return True