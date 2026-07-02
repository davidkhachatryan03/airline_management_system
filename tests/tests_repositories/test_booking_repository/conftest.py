import string, random
from datetime import datetime
from decimal import Decimal
import pytest
from uuid6 import uuid7

from src.common import DBManager
from src.core.repositories import BookingRepository
from src.entities import Booking

@pytest.fixture(scope="session")
def booking_repository(db_connected: DBManager) -> BookingRepository:
    return BookingRepository(db_connected)

def get_booking() -> Booking:
    return Booking(
        id=uuid7(),
        booking_reference=get_booking_reference(),
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

def get_booking_reference() -> str:
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=6))