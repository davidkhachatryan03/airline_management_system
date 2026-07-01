from datetime import date
import pytest, random

from src.common import DBManager
from src.core.repositories import PassengerRepository
from src.entities import Passenger

@pytest.fixture
def passenger_repository(db_connected: DBManager) -> PassengerRepository:
    return PassengerRepository(db_connected)

def get_national_identity_number() -> str:
    return str(random.randint(10000000, 60000000))

def get_passenger() -> Passenger:
    return Passenger.new_passenger(
        full_name="David Khachatryan",
        national_identity_number=get_national_identity_number(),
        issue_country="ARG",
        birth_date=date(2000,1,1),
        email="mail@example.com",
        phone_number="1123456789"
    )

@pytest.fixture
def passenger() -> Passenger:
    return get_passenger()

@pytest.fixture
def passengers(cant: int = 3) -> list[Passenger]:
    return [get_passenger() for _ in range(cant)]