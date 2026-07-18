from decimal import Decimal
from uuid import UUID

import pytest

from src.entities import Airplane


def test_airplane_valid_input(airplane: Airplane) -> None:

    assert airplane.id == 10
    assert airplane.tail_number == "ABC-123"
    assert airplane.manufacturer == "Airbus"
    assert airplane.model == "123-200"
    assert airplane.capacity == 132
    assert airplane.range_km == 6749
    assert airplane.flight_hour_cost_usd == Decimal("2000")
    assert airplane.current_status_id == 1