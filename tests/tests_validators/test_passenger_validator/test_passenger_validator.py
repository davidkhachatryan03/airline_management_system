from uuid import UUID

import pytest

from src.common.exceptions import BlacklistedPassenger, InexistentPassenger
from src.core.validators import PassengerValidator
from src.entities import Passenger

def test_passenger_validator_no_exception(passenger_validator: PassengerValidator, passengers_requested: list[Passenger], passengers_id_requested: list[UUID]) -> None:
    passenger_validator.check_existence(passengers_id_requested, passengers_requested)
    passenger_validator.check_blacklisted(passengers_requested)

def test_passenger_validator_blacklisted_passenger(passenger_validator: PassengerValidator, passenger_blacklisted: list[Passenger]) -> None:
    with pytest.raises(BlacklistedPassenger):
        passenger_validator.check_blacklisted(passenger_blacklisted)

def test_passenger_validator_inexistent_passenger_passengers_retrieved(passenger_validator: PassengerValidator, passengers_id_requested: list[UUID], passengers_retrieved: list[Passenger]) -> None:
    with pytest.raises(InexistentPassenger):
        passenger_validator.check_existence(passengers_id_requested, passengers_retrieved)

def test_passenger_validator_inexistent_passenger_no_passengers_retrieved(passenger_validator: PassengerValidator, passengers_id_requested: list[UUID]) -> None:
    with pytest.raises(InexistentPassenger):
        passenger_validator.check_existence(passengers_id_requested, [])