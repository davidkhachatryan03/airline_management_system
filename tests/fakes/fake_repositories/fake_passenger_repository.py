from uuid import UUID

from src.entities import Passenger

class FakePassengerRepository:

    def __init__(self) -> None:
        self.passengers: list[Passenger] = []

    def insert_passengers(self, passengers: list[Passenger]) -> None:
        self.passengers.extend(passengers)

    def retrieve_passengers_by_id(self, passengers_id: list[UUID]) -> list[Passenger]:
        return self.passengers
    
    def retrieve_passengers_by_document(self, passengers_document: list[tuple]) -> list[Passenger]:
        return self.passengers