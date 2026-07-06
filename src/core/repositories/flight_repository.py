from src.common import DBManager
from src.common.types import FlightRow, FlightId
from src.entities import Flight

class FlightRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager
    
    def insert_flights(self, flights: list[Flight]) -> None:
        self.db_manager.insert_rows("flights", flights)
    
    def retrieve_flights(self, limit: int = 5) -> list[Flight]:
        query = """
                SELECT  id, 
                        scheduled_departure_datetime, 
                        scheduled_arrival_datetime,
                        actual_departure_datetime,
                        actual_arrival_datetime,
                        operating_cost_usd,
                        base_price_usd,
                        current_status_id,
                        route_id,
                        airplane_id
                        FROM flights 
                        ORDER BY id DESC 
                        LIMIT %s
                """

        results: list[FlightRow] = self.db_manager.retrieve_many_columns(query, (limit,))

        if results:
            return [Flight(*result) for result in results]
        
        return []

    def retrieve_flights_by_id(self, flights_id: list[FlightId]) -> list[Flight]:
        if not flights_id:
            return []
        
        placeholders = ",".join(["%s" * len(flights_id)])

        query = """
                SELECT  id, 
                        scheduled_departure_datetime, 
                        scheduled_arrival_datetime,
                        actual_departure_datetime,
                        actual_arrival_datetime,
                        operating_cost_usd,
                        base_price_usd,
                        current_status_id,
                        route_id,
                        airplane_id
                FROM    flights
                WHERE   id 
                IN      ({})
                """.format(placeholders)
        
        result: list[FlightRow] = self.db_manager.retrieve_many_columns(query, flights_id)

        if result:
            return [Flight(*row) for row in result]
        
        return []
    
    def retrieve_seats_available_per_flight(self, flights: list[Flight]) -> dict[FlightId, int]:
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
        
        values: list[FlightId] = [flight.id for flight in flights]

        result: list[tuple[FlightId, int]] = self.db_manager.retrieve_many_columns(query, values)

        result_dict: dict[FlightId, int] = {}
        for row in result:
            result_dict[row[0]] = row[1]
        
        return result_dict