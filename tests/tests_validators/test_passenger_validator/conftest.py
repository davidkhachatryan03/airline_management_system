from datetime import date
from uuid import UUID

import pytest

from src.core.validators import PassengerValidator
from src.entities import Passenger

@pytest.fixture
def passengers_requested() -> list[Passenger]:
    passengers: list[Passenger] = []

    passenger_one = Passenger.new_passenger(
        full_name="David Khachatryan",
        national_identity_number="40123789",
        issue_country="ARG",
        birth_date=date(2000, 1, 1),
        email="dkh@email.com",
        phone_number="12345678"
    )

    passenger_two = Passenger.new_passenger(
        full_name="David Khachatryan",
        national_identity_number="40123789",
        issue_country="ARG",
        birth_date=date(2000, 1, 1),
        email="dkh@email.com",
        phone_number="12345678"
    )

    passengers.extend([passenger_one, passenger_two])

    return passengers

@pytest.fixture
def passenger_blacklisted(passengers_requested: list[Passenger]) -> list[Passenger]:
    passengers_requested[0].is_blacklisted = True

    return passengers_requested

@pytest.fixture
def passengers_id_requested(passengers_requested: list[Passenger]) -> list[UUID]:
    return [passenger.id for passenger in passengers_requested]

@pytest.fixture
def passengers_retrieved() -> list[Passenger]:
    passengers: list[Passenger] = []

    passenger_one = Passenger.new_passenger(
        full_name="John Doe",
        national_identity_number="12423",
        issue_country="USA",
        birth_date=date(1980, 1, 1),
        email="example@email.com",
        phone_number="12345678"
    )
    passenger_one.is_blacklisted = True

    passenger_two = Passenger.new_passenger(
        full_name="Lionel Messi",
        national_identity_number="4321667",
        issue_country="ARG",
        birth_date=date(2000, 1, 1),
        email="example@email.com",
        phone_number="12345678"
    )

    passengers.extend([passenger_one, passenger_two])

    return passengers

@pytest.fixture
def passenger_validator() -> PassengerValidator:
    return PassengerValidator()