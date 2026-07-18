from src.core.repositories import FlightRepository
from src.entities import Flight


def test_insert_flight(flight_repository: FlightRepository, flight: Flight) -> None:
    flight_repository.insert_flights([flight])

    last_inserted_flight: Flight = flight_repository.retrieve_flights(limit=1)[0]

    assert last_inserted_flight.id == flight.id
    assert (
        last_inserted_flight.scheduled_departure_datetime
        == flight.scheduled_departure_datetime
    )
    assert (
        last_inserted_flight.scheduled_arrival_datetime
        == flight._scheduled_arrival_datetime
    )
    assert (
        last_inserted_flight.actual_departure_datetime
        == flight.actual_departure_datetime
    )
    assert (
        last_inserted_flight.actual_arrival_datetime == flight.actual_arrival_datetime
    )
    assert last_inserted_flight.operating_cost_usd == flight.operating_cost_usd
    assert last_inserted_flight.base_price_usd == flight.base_price_usd
    assert last_inserted_flight.current_status_id == flight.current_status_id
    assert last_inserted_flight.route_id == flight.route_id
    assert last_inserted_flight.airplane_id == flight.airplane_id


def test_retrieve_all_flights(
    flight_repository: FlightRepository, flights: list[Flight]
) -> None:
    flight_repository.insert_flights(flights)

    all_inserted_flights: list[Flight] = flight_repository.retrieve_flights(limit=3)

    assert len(all_inserted_flights) == len(flights)
