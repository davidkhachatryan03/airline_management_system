from uuid import UUID

from src.common import DBManager
from src.entities import Passenger

class PassengerRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager

    def insert_passengers(self, passengers: list[Passenger]) -> None:
        self.db_manager.insert_rows("passengers", passengers)

    def retrieve_passengers_by_id(self, passengers_id: list[UUID]) -> list[Passenger]:
        if not passengers_id:
            return []
        
        placeholders = ",".join(["%s" * len(passengers_id)])

        query = """
                SELECT  *
                FROM    passengers
                WHERE   id IN ({})
                """.format(placeholders)
        
        values = passengers_id

        result: list[tuple] = self.db_manager.retrieve(query, values)

        if result:
            return [Passenger(*row) for row in result]
        
        return []
    
    def retrieve_passengers_by_document(self, passengers_document: list[tuple]) -> list[Passenger]:
        if not passengers_document:
            return []
        
        placeholders = ",".join(["%s" * len(passengers_document)])

        query = """
                SELECT  *
                FROM    passengers
                WHERE   (national_document_number) IN ({})
                """.format(placeholders)
        
        values = passengers_document

        result: list[tuple] = self.db_manager.retrieve(query, values)

        if result:
            return [Passenger(*row) for row in result]
        
        return []