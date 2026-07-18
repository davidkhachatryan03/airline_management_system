from datetime import datetime
from uuid import UUID

import pytest

from src.entities.boarding_pass import BoardingPass


def test_boarding_pass_valid_input(boarding_pass: BoardingPass) -> None:
    assert boarding_pass.id == UUID("019e92b3-e0db-7244-a9a2-43322a076e75")
    assert boarding_pass.issue_datetime == datetime(2024, 1, 1, 10, 0, 0)
    assert boarding_pass.boarding_datetime == datetime(2024, 1, 1, 10, 30, 0)
    assert boarding_pass.current_status_id == 1
    assert boarding_pass.ticket_id == UUID("019e97c2-2c47-73ad-8730-18e7d13cfbf7")


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
def test_invalid_boarding_pass(
    boarding_pass: BoardingPass, field, value, exception, message
) -> None:
    test_data: dict = boarding_pass.to_dict()
    test_data[field] = value

    with pytest.raises(exception, match=message):
        BoardingPass(**test_data)