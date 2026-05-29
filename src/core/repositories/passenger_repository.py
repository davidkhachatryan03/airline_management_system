from src.common import DBManager
from src.entities import Passenger
from src.api.schemas import PassengerRequest

class PassengerRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager