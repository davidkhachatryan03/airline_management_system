from src.common.types import FlightId, FlightIdentityKey
from src.core.repositories import FlightRepository
from src.entities import Flight


def test_insert_flight(
    flight_repository: FlightRepository, flights: list[Flight]
) -> None:
    flight_repository.insert_flights(flights)

    last_inserted_flights: list[Flight] = flight_repository.retrieve_flights(limit=5)

    assert set(last_inserted_flights) == set(flights)


def test_retrieve_all_flights(
    flight_repository: FlightRepository, flights: list[Flight]
) -> None:
    flight_repository.insert_flights(flights)

    all_inserted_flights: list[Flight] = flight_repository.retrieve_flights(limit=3)

    assert len(all_inserted_flights) == len(flights)


def test_retrieve_flights_by_id(
    flight_repository: FlightRepository, flights: list[Flight]
) -> None:
    flight_repository.insert_flights(flights)

    flight_ids: list[FlightId] = [flight.id for flight in flights]

    flights_retrieved: list[Flight] = flight_repository.retrieve_flights_by_ids(
        flight_ids
    )

    assert set(flights) == set(flights_retrieved)


def test_retrieve_flights_by_identity_key(
    flight_repository: FlightRepository, flights: list[Flight]
) -> None:
    flight_repository.insert_flights(flights)

    flight_identity_keys: list[FlightIdentityKey] = [
        flight.identity_key for flight in flights
    ]

    flights_retrieved: list[Flight] = (
        flight_repository.retrieve_flights_by_identity_keys(flight_identity_keys)
    )

    assert set(flights) == set(flights_retrieved)


def test_retrieve_seats_available_per_flight(
    flight_repository: FlightRepository,
    flights: list[Flight],
    seats_available_per_flight_expected: dict[FlightId, int],
) -> None:
    flight_repository.insert_flights(flights)

    flight_ids: list[FlightId] = [flight.id for flight in flights]

    seats_available_per_flight: dict[FlightId, int] = (
        flight_repository.retrieve_seats_available_per_flight(flight_ids)
    )

    assert seats_available_per_flight == seats_available_per_flight_expected
