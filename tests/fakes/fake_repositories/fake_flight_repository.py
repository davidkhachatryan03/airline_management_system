from src.common.types import FlightId
from src.entities import Flight
from tests.fakes.fake_repositories.fake_base_repository import FakeBaseRepository


class FakeFlightRepository(FakeBaseRepository[Flight]):

    def __init__(self) -> None:
        super().__init__()
        self.seats_available_per_flight: dict[FlightId, int] = {}

    def insert(self, flights: list[Flight]) -> None:
        super().insert(flights)
        for flight in flights:
            self.seats_available_per_flight[flight.id] = 10

    def retrieve_seats_available_per_flight(
        self, flight_ids: list[FlightId]
    ) -> dict[FlightId, int]:
        return {
            flight_id: self.seats_available_per_flight[flight_id]
            for flight_id in flight_ids
        }
