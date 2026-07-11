from src.common.types import FlightId, FlightIdentityKey, CurrentStatusId

class FlightValidator:

    def check_existence(self, flights_requested: list[FlightId], flights_retrieved: list[FlightId]) -> bool:
        missing_ids = set(flights_requested) - set(flights_retrieved)
        
        if missing_ids:
            return False
            
        return True
    
    def check_existente_by_identity_key(self, flights_requested: list[FlightIdentityKey], flights_retrieved: list[FlightIdentityKey]) -> bool:
        requested_ids = set(flights_requested)
        retrieved_ids = {flight for flight in flights_retrieved}
        
        missing_ids = requested_ids - retrieved_ids
        
        if missing_ids:
            return False
            
        return True
    
    def check_seats_available(self, seats_available_per_flight: dict[FlightId, int], number_of_passengers: int) -> bool:
        for flight in seats_available_per_flight:
            if seats_available_per_flight[flight] < number_of_passengers:
                return False
        
        return True
            
    def check_statuses(self, flights_retrieved_statuses: list[CurrentStatusId]) -> bool:
        for status in flights_retrieved_statuses:
            if status != 1: 
                return False
        
        return True