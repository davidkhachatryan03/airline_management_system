from uuid import UUID

import pytest

from src.common.types import CurrentStatusId, FlightId, RowId, RowIdentityKey
from src.core.validators import BaseValidator, FlightValidator


@pytest.fixture
def base_validator() -> BaseValidator:
    return BaseValidator()

@pytest.fixture
def flight_validator() -> FlightValidator:
    return FlightValidator()

@pytest.fixture
def ids_int_one() -> list[RowId]:
    return [1,2,3,4]

@pytest.fixture
def ids_int_two() -> list[RowId]:
    return [1,2,3,99]

@pytest.fixture
def ids_uuid_one() -> list[RowId]:
    return [UUID("019f5bde-6af2-7383-bd1b-dd5954d4e3aa"),
            UUID("019f5bdf-2240-7424-87a9-c42508929ae8"),
            UUID("019f5bdf-4768-7956-9dad-cd7c3c2c3d51")]

@pytest.fixture
def ids_uuid_two() -> list[RowId]:
    return [UUID("019f5bde-6af2-7383-bd1b-dd5954d4e3aa"),
            UUID("019f5bdf-2240-7424-87a9-c42508929ae8"),
            UUID("019f5be0-4d7f-7677-bc9e-ec3d9c733189")]

@pytest.fixture
def identity_keys_one() -> list[RowIdentityKey]:
    return [("A","B"), ("C","D")]

@pytest.fixture
def identity_keys_two() -> list[RowIdentityKey]:
    return [("E","F"), ("G","H")]

@pytest.fixture
def statuses_all_True() -> list[CurrentStatusId]:
    return [1,1,1,1,1]

@pytest.fixture
def statuses_mixed() -> list[CurrentStatusId]:
    return [0,1,1,1]

@pytest.fixture
def seats_available_per_flight() -> dict[FlightId, int]:
    return {
        UUID("019f5bde-6af2-7383-bd1b-dd5954d4e3aa"): 10,
        UUID("019f5bdf-2240-7424-87a9-c42508929ae8"): 2,
        UUID("019f6cb0-752b-7a55-acdc-fdf10e26965b"): 4
    }