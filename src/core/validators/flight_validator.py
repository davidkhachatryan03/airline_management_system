from uuid import UUID

from src.common.exceptions import FullFlight, InexistentFlight, NotScheduledFlight, DuplicatedFlight
from src.entities import Flight

class FlightValidator:

    def check_flights_existence(self, flights_requested: list[UUID], flights_retrieved: list[Flight]) -> None:
        if not flights_retrieved:
            raise InexistentFlight

        flights_requested_set = set(flights_requested)
        for flight in flights_retrieved:
            if flight.id not in flights_requested_set:
                raise InexistentFlight
        
    def check_flight_not_existence(self, flight_retrieved: Flight) -> None:
        if flight_retrieved:
            raise DuplicatedFlight
    
    def check_seats_available_per_flight(self, seats_available_per_flight: dict[UUID, int], number_of_passengers: int) -> None:
        for flight in seats_available_per_flight:
            if seats_available_per_flight[flight] < number_of_passengers:
                raise FullFlight
            
    def check_flights_statuses(self, flights_retrieved: list[Flight]) -> None:
        for flight in flights_retrieved:
            if flight.current_status_id != 1: 
                raise NotScheduledFlight
    
    def check_flight_to_register(self) -> None:
        pass