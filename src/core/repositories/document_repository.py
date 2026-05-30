from src.common import DBManager
from src.entities import Document
from src.api.schemas import PassengerRequest

class DocumentRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager

    def retrieve_documents(self, documents_requested: list[tuple]) -> list[Document]:
        if not documents_requested:
            return []
        
        placeholders = ",".join(["(" + ",".join(["%s"] * len(documents_requested[0])) + ")"] * len(documents_requested))

        query = """
                SELECT  *
                FROM    documents
                WHERE   (document_number, valid_from, valid_until, issue_country, document_type_id)
                IN      ({})
                """.format(placeholders)
        
        values: list = [value for document in documents_requested for value in document]

        result: list[tuple] = self.db_manager.retrieve(query, values)

        if result:
            return [Document(*row) for row in result]
        
        return []
    
    def insert_documents(self, documents: list[Document]) -> None:
        self.db_manager.insert_rows("documents" ,documents)