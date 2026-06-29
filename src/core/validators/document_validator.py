from src.common.exceptions import DuplicatedDocument
from src.entities import Document

class DocumentValidator:

    def check_existence(self, documents_requested: list[tuple], documents_retrieved: list[Document]) -> None:
        if len(documents_retrieved) != len(documents_requested):
            raise DuplicatedDocument