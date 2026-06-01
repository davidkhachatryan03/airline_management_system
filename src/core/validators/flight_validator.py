from src.common.exceptions import InvalidFlightId, FullFlight, NotProgrammedFlight
from uuid import UUID
from src.entities import Flight

class FlightValidator:

    def check_flights_existence(self, flights_requested: list[UUID], flights_retrieved: list[Flight]) -> None:
        set_flights_requested = set(flights_requested)
        for flight in flights_retrieved:
            if flight.id not in set_flights_requested:
                raise InvalidFlightId
    
    def check_seats_available_per_flight(self, seats_available_per_flight: list[tuple[UUID, int]], number_of_passengers: int) -> None:
        for seats in seats_available_per_flight:
            if seats[1] < number_of_passengers:
                raise FullFlight
            
    def check_flights_statuses(self, flights_retrieved: list[Flight]) -> None:
        for flight in flights_retrieved:
            raise NotProgrammedFlight