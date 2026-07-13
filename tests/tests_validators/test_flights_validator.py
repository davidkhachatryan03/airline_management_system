from src.common.types import FlightId
from src.core.validators import FlightValidator

def test_check_seats_available(flight_validator: FlightValidator, seats_available_per_flight: dict[FlightId, int]) -> None:
    number_of_passengers = 1

    assert flight_validator.check_seats_available(seats_available_per_flight, number_of_passengers)

    number_of_passengers = 99999999999

    assert not flight_validator.check_seats_available(seats_available_per_flight, number_of_passengers)