from datetime import datetime

import pytest
from uuid6 import uuid7

from src.entities.boarding_pass import BoardingPass


@pytest.fixture
def data():
    return {
        "id": uuid7(),
        "issue_datetime": datetime(2024, 1, 1, 10, 0, 0),
        "boarding_datetime": datetime(2024, 1, 1, 10, 30, 0),
        "current_status_id": 1,
        "ticket_id": uuid7(),
    }


def test_boarding_pass_valid_input(data) -> None:
    boarding_pass = BoardingPass(**data)

    assert boarding_pass.to_dict() == data


@pytest.mark.parametrize(
    "field, value, exception, message",
    [
        ("id", 123, TypeError, "The type of 123 is not UUID."),
        (
            "issue_datetime",
            "2024-01-01 10:00:00",
            TypeError,
            "The type of 2024-01-01 10:00:00 is not datetime.",
        ),
        (
            "boarding_datetime",
            "2024-01-01 10:30:00",
            TypeError,
            "The type of 2024-01-01 10:30:00 must be datetime or none.",
        ),
        (
            "current_status_id",
            "1",
            TypeError,
            "The type of 1 is not int.",
        ),
        (
            "current_status_id",
            0,
            ValueError,
            "The current status id can not be negative or zero.",
        ),
        (
            "current_status_id",
            -10,
            ValueError,
            "The current status id can not be negative or zero.",
        ),
        ("ticket_id", 123, TypeError, "The type of 123 is not UUID."),
    ],
)
def test_invalid_boarding_pass(data, field, value, exception, message) -> None:
    data[field] = value

    with pytest.raises(exception, match=message):
        BoardingPass(**data)
