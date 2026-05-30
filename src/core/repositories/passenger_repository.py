from src.common import DBManager
from src.entities import Passenger
from src.api.schemas import PassengerRequest

class PassengerRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager

    def insert_passengers(self, passengers: list[Passenger]) -> None:
        self.db_manager.insert_rows("passengers", passengers)