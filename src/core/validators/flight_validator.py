from src.common.types import FlightId, CurrentStatusId

class FlightValidator:
    
    def check_seats_available(self, seats_available_per_flight: dict[FlightId, int], number_of_passengers: int) -> bool:
        for flight in seats_available_per_flight:
            if seats_available_per_flight[flight] < number_of_passengers:
                return False
        
        return True