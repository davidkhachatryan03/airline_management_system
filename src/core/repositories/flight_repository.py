from src.common import DBManager
from src.entities import Flight
from uuid import UUID

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
        
        result: list[tuple] = self.db_manager.retrieve(query, flights_id)

        if result:
            return [Flight(*row) for row in result]
        
        return []
    
    def retrieve_seats_available_per_flight(self, flights: list[Flight]) -> list[tuple[UUID, int]]:
        if not flights:
            return []
        
        placeholders = "(" + "".join(["%s" * len(flights)]) + ")"

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
        
        flights_id: list[UUID] = [flight.id for flight in flights]
        result: list[tuple[UUID, int]] = self.db_manager.retrieve(query, flights_id)

        if result:
            return result
        
        return []