import os

import pytest

from src.common import DBManager
from src.core.repositories import (
    AirplaneRepository,
    BookingRepository,
    DocumentRepository,
    FlightRepository,
    PassengerRepository,
    RouteRepository,
    TicketRepository,
)
from src.core.validators import BaseValidator, FlightValidator
from tests.factories import (
    AirplaneFactory,
    BoardingPassFactory,
    BookingFactory,
    DocumentFactory,
    FlightFactory,
    PassengerFactory,
    RouteFactory,
    TicketFactory,
)
from tests.fakes.fake_repositories import (
    FakeBookingRepository,
    FakeDocumentRepository,
    FakePassengerRepository,
)

os.environ["TESTING"] = "True"


@pytest.fixture
def db() -> DBManager:
    return DBManager()


@pytest.fixture(scope="session", autouse=True)
def db_connected():
    db = DBManager()

    with db:
        yield db


@pytest.fixture(autouse=True)
def revert_changes(db_connected: DBManager):
    db_connected.connection.start_transaction()

    yield db_connected

    db_connected.connection.rollback()


@pytest.fixture
def airplane_repository(db_connected: DBManager) -> AirplaneRepository:
    return AirplaneRepository(db_connected)


@pytest.fixture()
def booking_repository(db_connected: DBManager) -> BookingRepository:
    return BookingRepository(db_connected)


@pytest.fixture
def document_repository(db_connected: DBManager) -> DocumentRepository:
    return DocumentRepository(db_connected)


@pytest.fixture
def flight_repository(db_connected: DBManager) -> FlightRepository:
    return FlightRepository(db_connected)


@pytest.fixture
def passenger_repository(db_connected: DBManager) -> PassengerRepository:
    return PassengerRepository(db_connected)


@pytest.fixture
def route_repository(db_connected: DBManager) -> RouteRepository:
    return RouteRepository(db_connected)


@pytest.fixture
def ticket_repository(db_connected: DBManager) -> TicketRepository:
    return TicketRepository(db_connected)


@pytest.fixture
def fake_booking_repository() -> FakeBookingRepository:
    return FakeBookingRepository()


@pytest.fixture
def fake_document_repository() -> FakeDocumentRepository:
    return FakeDocumentRepository()


@pytest.fixture
def fake_passenger_repository() -> FakePassengerRepository:
    return FakePassengerRepository()


@pytest.fixture
def base_validator() -> BaseValidator:
    return BaseValidator()


@pytest.fixture
def flight_validator() -> FlightValidator:
    return FlightValidator()


@pytest.fixture(autouse=True)
def reset_factory_sequences() -> None:
    AirplaneFactory.reset_sequence(0)
    BoardingPassFactory.reset_sequence(0)
    BookingFactory.reset_sequence(0)
    DocumentFactory.reset_sequence(0)
    FlightFactory.reset_sequence(0)
    PassengerFactory.reset_sequence(0)
    RouteFactory.reset_sequence(0)
    TicketFactory.reset_sequence(0)
