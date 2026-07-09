from src.common.types import FlightId
from src.entities import Flight

class FlightValidator:

    def check_existence(self, flights_requested: list[FlightId], flights_retrieved: list[Flight]) -> bool:
        requested_ids = set(flights_requested)
        retrieved_ids = {flight.id for flight in flights_retrieved}
        
        missing_ids = requested_ids - retrieved_ids
        
        if missing_ids:
            return False
            
        return True
    
    def check_seats_available(self, seats_available_per_flight: dict[FlightId, int], number_of_passengers: int) -> bool:
        for flight in seats_available_per_flight:
            if seats_available_per_flight[flight] < number_of_passengers:
                return False
        
        return True
            
    def check_statuses(self, flights_retrieved: list[Flight]) -> bool:
        for flight in flights_retrieved:
            if flight.current_status_id != 1: 
                return False
        
        return True