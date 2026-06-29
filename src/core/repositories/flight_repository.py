from uuid import UUID

from src.common import DBManager
from src.entities import Flight

class FlightRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager
        

    def retrieve_flights_by_id(self, flights_id: list[UUID]) -> list[Flight]:
        if not flights_id:
            return []
        
        placeholders = ",".join(["%s" * len(flights_id)])

        query = """
                SELECT  *
                FROM    flights
                WHERE   id 
                IN      ({})
                """.format(placeholders)
        
        values = flights_id

        result: list[tuple] = self.db_manager.retrieve(query, values)

        if result:
            return [Flight(*row) for row in result]
        
        return []
    
    def retrieve_seats_available_per_flight(self, flights: list[Flight]) -> dict[UUID, int]:
        if not flights:
            return {}
        
        placeholders = "".join(["%s" * len(flights)])

        query = """
                SELECT      f.id, 
                            (a.capacity - COUNT(t.id)) AS asientos_disponibles
                FROM        flights f
                JOIN        airplanes a 
                ON          f.airplane_id = a.id
                LEFT JOIN   tickets t 
                ON          t.flight_id = f.id 
                AND         t.current_status_id = 1 
                WHERE       f.id 
                IN          ({}) 
                GROUP BY    f.id, 
                            a.capacity;
                """.format(placeholders)
        
        values: list[UUID] = [flight.id for flight in flights]

        result: list[tuple[UUID, int]] = self.db_manager.retrieve(query, values)

        result_dict: dict[UUID, int] = {}
        for row in result:
            result_dict[row[0]] = row[1]
        
        return result_dict