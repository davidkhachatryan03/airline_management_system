import pytest

from src.api.schemas import FlightRequest
from src.core.units_of_work import RegisterDocumentUoW
from src.core.use_cases import RegisterDocument, RegisterDocumentValidator
from src.entities import Flight
from tests.fakes.fake_uows.fake_register_flight_uow import FakeRegisterFlightUoW
from tests.fakes.fake_db_manager import FakeDBManager

def test_register_flight_valid_input(flight_generated: Flight) -> None:
    fake_uow = FakeRegisterFlightUoW(FakeDBManager())

    

def test_register_flight_inexistent_airplane() -> None:
    pass

def test_register_flight_unavailable_airplane() -> None:
    pass

def test_register_flight_inexistent_route() -> None:
    pass

def test_register_flight_duplicated_flight() -> None:
    pass

def test_register_flight_multiple_exceptions() -> None: 
    pass