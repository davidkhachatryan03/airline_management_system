import random
from datetime import date, datetime
from decimal import Decimal
import pytest
from uuid6 import uuid7
from uuid import UUID

from src.common import DBManager
from src.core.repositories import BookingRepository, DocumentRepository, PassengerRepository
from src.entities import Booking, Document, Passenger

@pytest.fixture(scope="session", autouse=True)
def db_connected():
    db = DBManager()

    with db:
        yield db

@pytest.fixture(scope="function", autouse=True)
def revert_changes(db_connected: DBManager):
    db_connected.connection.start_transaction()

    yield db_connected

    db_connected.connection.rollback()

@pytest.fixture(scope="session")
def booking_repository(db_connected: DBManager) -> BookingRepository:
    return BookingRepository(db_connected)

def get_booking() -> Booking:
    return Booking(
        id=uuid7(),
        booking_reference=Booking._generate_reference(),
        booking_datetime=datetime.now(),
        paid_amount_usd=Decimal("10000"),
        current_status_id=1
    )

@pytest.fixture
def booking() -> Booking:
    return get_booking()

@pytest.fixture
def bookings(cant:int = 3) -> list[Booking]:
    return [get_booking() for _ in range(cant)]

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

@pytest.fixture
def document_repository(db_connected: DBManager) -> DocumentRepository:
    return DocumentRepository(db_connected)

def get_document(passenger_id: UUID) -> Document:
    return Document.new_document(
        document_number=get_national_identity_number(),
        valid_from=date(2020,1,1),
        valid_until=date(2030,1,1),
        issue_country="ARG",
        passenger_id=passenger_id,
        document_type_id=1
    )

@pytest.fixture
def document(passenger: Passenger) -> Document:
    return get_document(passenger.id)

@pytest.fixture
def documents(passengers: list[Passenger]) -> list[Document]:
    return [get_document(passenger.id) for passenger in passengers]