from datetime import date
import pytest
from uuid import UUID

from src.common import DBManager
from src.core.repositories import FlightRepository
from src.entities import Flight

@pytest.fixture
def flight_repository(db_connected: DBManager) -> FlightRepository:
    return FlightRepository(db_connected)

