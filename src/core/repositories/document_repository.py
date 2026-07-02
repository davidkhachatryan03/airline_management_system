from src.common import DBManager
from src.entities import Document

class DocumentRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager
    
    def insert_documents(self, documents: list[Document]) -> None:
        self.db_manager.insert_rows("documents", documents)

    def retrieve_documents(self, limit: int = 5) -> list[Document]:
        query = "SELECT * FROM documents ORDER BY id DESC LIMIT %s"

        results: list[tuple] = self.db_manager.retrieve(query, (limit,))

        if results:
            return [Document(*result) for result in results]
        
        return []

    def retrieve_documents_by_identity_key(self, documents_requested: list[tuple]) -> list[Document]:
        if not documents_requested:
            return []
        
        placeholders = ",".join(["(" + ",".join(["%s"] * len(documents_requested[0])) + ")"] * len(documents_requested))

        query = """
                SELECT  *
                FROM    documents
                WHERE   (document_number, issue_country)
                IN      ({})
                """.format(placeholders)
        
        values: list = [value for document in documents_requested for value in document]

        result: list[tuple] = self.db_manager.retrieve(query, values)

        if result:
            return [Document(*row) for row in result]
        
        return []