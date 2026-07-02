import random
from datetime import date, datetime
from decimal import Decimal
import pytest
from uuid6 import uuid7
from uuid import UUID

from src.common import DBManager
from src.core.repositories import BookingRepository, DocumentRepository, FlightRepository, PassengerRepository, TicketRepository
from src.entities import Booking, Document, Flight, Passenger, Ticket

@pytest.fixture
def db() -> DBManager:
    return DBManager()

@pytest.fixture(scope="session", autouse=True)
def db_connected():
    db = DBManager()

    with db:
        yield db

@pytest.fixture
def airline_test() -> str:
    return "airline_test"

@pytest.fixture(autouse=True)
def revert_changes(db_connected: DBManager):
    db_connected.connection.start_transaction()

    yield db_connected

    db_connected.connection.rollback()

@pytest.fixture()
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

@pytest.fixture
def flight_repository(db_connected: DBManager) -> FlightRepository:
    return FlightRepository(db_connected)

def get_flight(route_id: int = 1) -> Flight:
    flight = Flight.new_flight(
        scheduled_departure_datetime=datetime(2026,1,1,13,10),
        scheduled_arrival_datetime=datetime(2026,1,1,17,42),
        operating_cost_usd=Decimal("8700"),
        route_id=route_id,
        airplane_id=1
    )
    flight.id = uuid7()

    return flight

@pytest.fixture
def flight() -> Flight:
    return get_flight()

@pytest.fixture
def flights() -> list[Flight]:
    return [get_flight(route_id=2), get_flight(route_id=3), get_flight(route_id=4)]

@pytest.fixture
def ticket_repository(db_connected: DBManager) -> TicketRepository:
    return TicketRepository(db_connected)

def get_ticket(booking_id: UUID, flight_id: UUID, passenger_id: UUID) -> Ticket:
    return Ticket.new_ticket(
        paid_amount_usd=Decimal(10000),
        booking_id=booking_id,
        flight_id=flight_id,
        passenger_id=passenger_id
    )

@pytest.fixture
def ticket(booking: Booking, flight: Flight, passenger: Flight) -> Ticket:
    return get_ticket(booking.id, flight.id, passenger.id)

@pytest.fixture
def tickets(booking: Booking, flight: Flight, passengers: list[Passenger]) -> list[Ticket]:
    return [get_ticket(booking.id, flight.id, passenger.id) for passenger in passengers]

@pytest.fixture
def sql_file_route() -> str:
    return "tests/fakes/fake_sql_file.sql"

@pytest.fixture
def uuid_list(cant: int = 10) -> list[UUID]:
    return [uuid7() for _ in range(cant)]

@pytest.fixture
def uuid_bytes_list(uuid_list: list[UUID]) -> list[bytes]:
    return [uuid.bytes for uuid in uuid_list]

@pytest.fixture
def invalid_uuid_bytes_list(cant: int = 10) -> list:
    return [(uuid7(), b"1234567890123456", uuid7()) for _ in range(cant)]

@pytest.fixture
def random_rows_retrieved() -> list[tuple]:
    return [(uuid7().bytes, 1, "ABC", 12), (uuid7().bytes, 99, "CDE", 90)]

@pytest.fixture
def random_rows_retrieved_invalid_bytes() -> list[tuple]:
    return [(uuid7().bytes, 1, "ABC", 12), (uuid7().bytes, 99, "CDE", 90, b"1234567890123456")]