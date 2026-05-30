from src.common.exceptions import InvalidFlightId
from uuid import UUID
from src.entities import Flight

class FlightValidator:

    def check_flights_existence(self, flights_requested: list[UUID], flights_retrieved: list[Flight]) -> None:
        set_flights_requested = set(flights_requested)
        for flight in flights_retrieved:
            if flight.id not in set_flights_requested:
                raise InvalidFlightId(f"{flight.id} is not registered.")
    
    def check_seats_available_per_flight(self, seats_available_per_flight: list[tuple[UUID, int]], number_of_passengers: int) -> None:
        for seats in seats_available_per_flight:
            if seats[1] < number_of_passengers:
                raise InvalidFlightId(f"Flight {seats[0]} has less available seats than required.")