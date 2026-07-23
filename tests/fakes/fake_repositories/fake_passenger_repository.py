from src.common.types import PassengerId
from src.entities import Passenger


class FakePassengerRepository:

    def __init__(self) -> None:
        self.passengers: list[Passenger] = []

    def insert_passengers(self, passengers: list[Passenger]) -> None:
        self.passengers.extend(passengers)

    def retrieve_passengers_by_ids(
        self, passenger_ids: list[PassengerId]
    ) -> list[Passenger]:
        passengers_retrieved: list[Passenger] = []

        passenger_stored_ids: dict[PassengerId, Passenger] = {
            passenger.id: passenger for passenger in self.passengers
        }
        for passenger_id in passenger_ids:
            if passenger_id in passenger_stored_ids:
                passengers_retrieved.append(passenger_stored_ids[passenger_id])

        return passengers_retrieved
