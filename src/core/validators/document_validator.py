from src.common.exceptions import DuplicatedDocument
from src.entities import Document

class DocumentValidator:

    def check_existence(self, documents_requested: list[tuple], documents_retrieved: list[Document]) -> None:
        for document in documents_retrieved:
            if document.identity_key in documents_requested:
                raise DuplicatedDocument