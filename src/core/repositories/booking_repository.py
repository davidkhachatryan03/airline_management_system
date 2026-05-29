from src.common import DBManager

class BookingRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager  