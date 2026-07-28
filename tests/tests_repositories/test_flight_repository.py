from src.common.types import FlightId
from src.core.repositories import FlightRepository
from src.entities import Flight


def test_retrieve_seats_available_per_flight(
    flight_repository: FlightRepository, flights: list[Flight]
) -> None:
    flight_repository.insert(flights)

    flight_ids: list[FlightId] = [flight.id for flight in flights]

    seats_available_per_flight: dict[FlightId, int] = (
        flight_repository.retrieve_seats_available_per_flight(flight_ids)
    )

    seats_available_per_flight_expected: dict[FlightId, int] = {
        flight.id: 18 for flight in flights
    }

    assert seats_available_per_flight == seats_available_per_flight_expected
