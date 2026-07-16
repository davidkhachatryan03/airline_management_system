from src.common.types import FlightId
from src.core.validators import FlightValidator

def test_check_seats_available_full_flight(flight_validator: FlightValidator, seats_available_per_flight: dict[FlightId, int]) -> None:
    first_flight: FlightId = list(seats_available_per_flight.keys())[0]
    seats_available_per_flight[first_flight] = 0

    full_flights, not_seats_enough = flight_validator.check_seats_available(seats_available_per_flight, number_of_passengers=1)

    assert len(full_flights) == 1
    assert len(not_seats_enough) == 0

def test_check_seats_available_not_seats_enough(flight_validator: FlightValidator, seats_available_per_flight: dict[FlightId, int]) -> None:
    full_flights, not_seats_enough = flight_validator.check_seats_available(seats_available_per_flight, number_of_passengers=999)

    assert len(full_flights) == 0
    assert len(not_seats_enough) == 3

def test_check_seats_available_full_flight_and_not_seats_enough(flight_validator: FlightValidator, seats_available_per_flight: dict[FlightId, int]) -> None:
    first_flight: FlightId = list(seats_available_per_flight.keys())[0]
    seats_available_per_flight[first_flight] = 0

    full_flights, not_seats_enough = flight_validator.check_seats_available(seats_available_per_flight, number_of_passengers=999)

    assert len(full_flights) == 1
    assert len(not_seats_enough) == 2