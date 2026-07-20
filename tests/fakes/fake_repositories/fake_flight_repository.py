from src.common.types import FlightId, FlightIdentityKey
from src.entities import Flight


class FakeFlightRepository:

    def __init__(self) -> None:
        self.flights: dict[Flight, int] = {}

    def insert_flights(self, flights: list[Flight], seats: int = 10) -> None:
        for flight in flights:
            self.flights[flight] = seats

    def retrieve_flights_by_id(self, flight_ids: list[FlightId]) -> list[Flight]:
        flights_retrieved: list[Flight] = []

        flight_stored_ids: dict[FlightId, Flight] = {flight.id: flight for flight in self.flights}
        for flight_id in flight_ids:
            if flight_id in flight_stored_ids:
                flights_retrieved.append(flight_stored_ids[flight_id])
        
        return flights_retrieved

    def retrieve_flights_by_identity_key(
        self, flights: list[FlightIdentityKey]
    ) -> list[Flight]:
        flights_retrieved: list[Flight] = []
        flights_stored: list[Flight] = list(self.flights.keys())

        flight_stored_identity_keys: dict[FlightIdentityKey, Flight] = {
            flight.identity_key: flight for flight in flights_stored
        }
        for flight in flights:
            if flight in flight_stored_identity_keys:
                flights_retrieved.append(flight_stored_identity_keys[flight])

        return flights_retrieved

    def retrieve_seats_available_per_flight(
        self, flights: list[Flight]
    ) -> dict[FlightId, int]:
        seats_available_per_flight: dict[FlightId, int] = {}
        
        flights_stored: list[Flight] = list(self.flights.keys())
        for flight in flights_stored:
            seats_available_per_flight[flight.id] = self.flights[flight]

        return seats_available_per_flight
