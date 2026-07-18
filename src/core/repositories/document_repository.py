from src.common import DBManager
from src.common.types import DocumentIdentityKey, DocumentRow
from src.entities import Document


class DocumentRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager
    
    def insert_documents(self, documents: list[Document]) -> None:
        self.db_manager.insert_rows("documents", documents)

    def retrieve_documents(self, limit: int = 5) -> list[Document]:
        query = "SELECT id, document_number, valid_from, valid_until, issue_country, passenger_id, document_type_id FROM documents ORDER BY id DESC LIMIT %s"

        results: list[DocumentRow] = self.db_manager.retrieve_many_columns(query, (limit,))

        if results:
            return [Document(*result) for result in results]
        
        return []

    def retrieve_documents_by_identity_key(self, documents_requested: list[DocumentIdentityKey]) -> list[Document]:
        if not documents_requested:
            return []
        
        placeholders = ",".join(["(" + ",".join(["%s"] * len(documents_requested[0])) + ")"] * len(documents_requested))

        query = """
                SELECT  id,
                        document_number,
                        valid_from,
                        valid_until,
                        issue_country,
                        passenger_id,
                        document_type_id
                FROM    documents
                WHERE   (document_number, issue_country)
                IN      ({})
                """.format(placeholders)
        
        values = [value for document in documents_requested for value in document]

        result: list[DocumentRow] = self.db_manager.retrieve_many_columns(query, values)

        if result:
            return [Document(*row) for row in result]
        
        return []