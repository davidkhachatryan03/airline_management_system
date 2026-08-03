from datetime import date

import pytest
from uuid6 import uuid7

from src.entities import Passenger


@pytest.fixture
def data():
    return {
        "id": uuid7(),
        "full_name": "David Khachatryan",
        "birth_date": date(2000, 1, 1),
        "email": "example@mail.com",
        "phone_number": "123456789",
        "is_blacklisted": False,
        "is_vip": False,
    }


def test_passenger_valid_input(data) -> None:
    passenger = Passenger(**data)

    assert passenger.to_dict() == data


def test_new_passenger_classmethod_valid_input(mocker, data) -> None:
    mocker.patch("src.entities.passenger.uuid7", return_value=data["id"])

    passenger = Passenger.new_passenger(
        full_name=data["full_name"],
        birth_date=data["birth_date"],
        email=data["email"],
        phone_number=data["phone_number"],
    )

    assert passenger.to_dict() == data


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
def test_invalid_passenger(data, field, value, exception, message) -> None:
    data[field] = value

    with pytest.raises(exception, match=message):
        Passenger(**data)
