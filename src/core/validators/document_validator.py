from src.common.types import DocumentIdentityKey

class DocumentValidator:

    def check_existence(self, documents_requested_identity_keys: list[DocumentIdentityKey], documents_retrieved_identity_keys: list[DocumentIdentityKey]) -> bool:
        missing_ids = set(documents_requested_identity_keys) - set(documents_retrieved_identity_keys)
        
        if missing_ids:
            return False
            
        return True