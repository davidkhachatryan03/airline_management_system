from src.common.types import FlightId
from src.entities import Flight


class FlightValidator:
    
    def check_seats_available(self, seats_available_per_flight: dict[FlightId, int], number_of_passengers: int) -> tuple[list[FlightId], list[FlightId]]:
        full_flights_ids: list[FlightId] = []
        not_seats_enough_flights_ids: list[FlightId] = []

        for flight in seats_available_per_flight:
            if seats_available_per_flight[flight] == 0:
                full_flights_ids.append(flight)

            elif seats_available_per_flight[flight] < number_of_passengers:
                not_seats_enough_flights_ids.append(flight) 
        
        return full_flights_ids, not_seats_enough_flights_ids
    
    def check_statuses(self, flights: list[Flight]) -> list[FlightId]:
        not_scheduled_flights: list[FlightId] = []

        for flight in flights:
            if flight.current_status_id != 1:
                not_scheduled_flights.append(flight.id)
            
        return not_scheduled_flights