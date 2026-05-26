from src.common import DBManager

class DocumentRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager