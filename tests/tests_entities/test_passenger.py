from datetime import date
from uuid import UUID

import pytest

from src.entities import Passenger


def test_passenger_valid_input(passenger: Passenger) -> None:

    assert passenger.id == UUID("019e92b3-e0db-7244-a9a2-43322a076e75")
    assert passenger.full_name == "David Khachatryan"
    assert passenger.birth_date == date(2000, 1, 1)
    assert passenger.email == "dkh@email.com"
    assert passenger.phone_number == "12345678"
    assert passenger.is_blacklisted is False
    assert passenger.is_vip is True


def test_new_passenger_classmethod_valid_input(passenger: Passenger) -> None:
    new_passenger = Passenger.new_passenger(
        full_name=passenger.full_name,
        birth_date=passenger.birth_date,
        email=passenger.email,
        phone_number=passenger.phone_number,
    )

    assert isinstance(new_passenger.id, UUID)
    assert new_passenger.full_name == passenger.full_name
    assert new_passenger.birth_date == passenger.birth_date
    assert new_passenger.email == passenger.email
    assert new_passenger.phone_number == passenger.phone_number
    assert new_passenger.is_blacklisted is False
    assert new_passenger.is_vip is False


@pytest.mark.parametrize(
    "field, value, exception, message",
    [
        ("id", 123, TypeError, "The type of the id is not UUID."),
        ("full_name", 123, TypeError, "The type of the full name is not str."),
        ("full_name", "   ", ValueError, "The full name can not be empty."),
        (
            "full_name",
            "A" * 101,
            ValueError,
            "The full name must be 100 characters long or less.",
        ),
        (
            "birth_date",
            "2000-01-01",
            TypeError,
            "The type of the birth date is not date.",
        ),
        ("email", 123, TypeError, "The type of the email is not str."),
        ("email", "   ", ValueError, "The email can not be empty."),
        (
            "email",
            "a" * 101,
            ValueError,
            "The full name must be 100 characters long or less.",
        ),
        ("phone_number", 123, TypeError, "The type of the phone number is not str."),
        ("phone_number", "   ", ValueError, "The phone number can not be empty."),
        (
            "phone_number",
            "1" * 21,
            ValueError,
            "The phone number must be 20 characters long or less.",
        ),
        (
            "is_blacklisted",
            "True",
            TypeError,
            "The type of the blacklisted value must be True, False, 1 or 0.",
        ),
        (
            "is_vip",
            2,
            TypeError,
            "The type of the vip value must be True, False, 1 or 0.",
        ),
    ],
)
def test_invalid_passenger(
    passenger: Passenger, field, value, exception, message
) -> None:
    test_data: dict = passenger.to_dict()
    test_data[field] = value

    with pytest.raises(exception, match=message):
        Passenger(**test_data)
