from datetime import date

import pytest

from src.api.schemas import PassengerRequest


@pytest.fixture
def passenger_request() -> PassengerRequest:
    return PassengerRequest(
        full_name="John Doe",
        birth_date=date(2000, 1, 1),
        email="example@mail.com",
        phone_number="123456789",
        document_number="987654321",
        valid_from=date(2020, 1, 1),
        valid_until=date(2030, 1, 1),
        issue_country="USA",
        document_type_id=1,
    )
