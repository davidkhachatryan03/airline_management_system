from src.common import DBManager
from src.common.types import PassengerRow, PassengerId, DocumentIdentityKey
from src.entities import Passenger

class PassengerRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager

    def insert_passengers(self, passengers: list[Passenger]) -> None:
        self.db_manager.insert_rows("passengers", passengers)

    def retrieve_passengers_by_id(self, passengers_id: list[PassengerId]) -> list[Passenger]:
        if not passengers_id:
            return []
        
        placeholders = ",".join(["%s" * len(passengers_id)])

        query = """
                SELECT  id, 
                        full_name, 
                        birth_date, 
                        email,
                        phone_number,
                        is_blacklisted,
                        is_vip
                FROM    passengers
                WHERE   id IN ({})
                """.format(placeholders)
        
        result: list[PassengerRow] = self.db_manager.retrieve_many_columns(query, passengers_id)

        if result:
            return [Passenger(*row) for row in result]
        
        return []
    
    def retrieve_passengers_by_document(self, documents_identity_keys: list[DocumentIdentityKey]) -> list[Passenger]:
        if not documents_identity_keys:
            return []
        
        placeholders = ",".join(["(" + ",".join(["%s"] * len(documents_identity_keys[0])) + ")"] * len(documents_identity_keys))

        query = """
                SELECT  p.id, 
                        p.full_name, 
                        p.birth_date, 
                        p.email,
                        p.phone_number,
                        p.is_blacklisted,
                        p.is_vip
                FROM    passengers p
                JOIN    documents d
                ON      p.id = d.passenger_id
                WHERE   (d.document_number, d.issue_country) IN ({})
                """.format(placeholders)
        
        result: list[PassengerRow] = self.db_manager.retrieve_many_columns(query, documents_identity_keys)

        if result:
            return [Passenger(*row) for row in result]
        
        return []
    
    def retrieve_passengers(self, limit: int = 5) -> list[Passenger]:
        query = """
                SELECT      id, 
                            full_name, 
                            birth_date, 
                            email,
                            phone_number,
                            is_blacklisted,
                            is_vip
                FROM        passengers 
                ORDER BY    id DESC 
                LIMIT       %s
                """

        results: list[PassengerRow] = self.db_manager.retrieve_many_columns(query, (limit,))
        
        if results:
            return [Passenger(*result) for result in results]
        
        return []