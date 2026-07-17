from collections.abc import KeysView
from uuid import UUID

from src.common.types import FlightIdentityKey
from src.entities import Flight

class FakeFlightRepository:

    def __init__(self) -> None:
        self.flights: dict[Flight, int] = {}

    def insert_flights(self, flights: list[Flight], seats: int=10) -> None:
        for flight in flights:
            self.flights[flight] = seats

    def retrieve_flights_by_id(self, flights_id: list[UUID]) -> list[Flight]:
        return list(self.flights.keys())
    
    def retrieve_flights_by_identity_key(self, flights: list[FlightIdentityKey]) -> list[Flight]:
        flights_retrieved: list[Flight] = []
        flights_stored: list[Flight] = list(self.flights.keys())
        dict_flights_stored_identity_keys: dict[FlightIdentityKey, Flight] = {flight.identity_key: flight for flight in flights_stored}

        for flight in flights:
            if flight in dict_flights_stored_identity_keys:
                flights_retrieved.append(dict_flights_stored_identity_keys[flight])
        
        return flights_retrieved
    
    def retrieve_seats_available_per_flight(self, flights: list[Flight]) -> dict[UUID, int]:
        flights_stored: KeysView[Flight] = self.flights.keys()
        seats_available_per_flight: dict[UUID, int] = {}

        for flight in flights_stored:
            seats_available_per_flight[flight.id] = self.flights[flight]

        return seats_available_per_flight