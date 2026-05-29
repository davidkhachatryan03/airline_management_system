from src.common import DBManager
from src.entities import Document
from src.api.schemas import PassengerRequest

class DocumentRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager