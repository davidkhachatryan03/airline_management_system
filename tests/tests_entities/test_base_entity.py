from decimal import Decimal
from uuid import UUID, uuid4

import pytest

from src.entities.base_entity import BaseEntity


class DummyFlight(BaseEntity):
    def __init__(self, id: UUID, flight_number: str):
        self.id = id
        self.flight_number = flight_number
        self._internal_db_state = "hidden"

    @property
    def id(self) -> UUID:
        return self._id

    @id.setter
    def id(self, value: UUID):
        self._id = value

    @property
    def flight_number(self) -> str:
        return self._flight_number

    @flight_number.setter
    def flight_number(self, value: str):
        self._flight_number = value


class DummyPassenger(BaseEntity):
    def __init__(self, full_name: str, identity_key: str):
        self.full_name = full_name
        self.identity_key = identity_key

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, value: str):
        self._full_name = value

    @property
    def identity_key(self) -> str:
        return self._identity_key

    @identity_key.setter
    def identity_key(self, value: str):
        self._identity_key = value


class DummyBooking(BaseEntity):
    def __init__(
        self,
        reference: str,
        amount: Decimal,
        flight: DummyFlight,
        passenger: DummyPassenger,
        flights_list: list[DummyFlight] = [],
    ):
        self.reference = reference
        self.amount = amount
        self.flight = flight
        self.passenger = passenger
        self.flights_list = flights_list if flights_list is not None else []

    @property
    def reference(self) -> str:
        return self._reference

    @reference.setter
    def reference(self, value: str):
        self._reference = value

    @property
    def amount(self) -> Decimal:
        return self._amount

    @amount.setter
    def amount(self, value: Decimal):
        self._amount = value

    @property
    def flight(self) -> DummyFlight:
        return self._flight

    @flight.setter
    def flight(self, value: DummyFlight):
        self._flight = value

    @property
    def passenger(self) -> DummyPassenger:
        return self._passenger

    @passenger.setter
    def passenger(self, value: DummyPassenger):
        self._passenger = value

    @property
    def flights_list(self) -> list[DummyFlight]:
        return self._flights_list

    @flights_list.setter
    def flights_list(self, value: list[DummyFlight]):
        self._flights_list = value

    def calculate_tax(self):
        return self.amount * Decimal("0.21")


@pytest.fixture
def sample_uuid():
    return uuid4()


@pytest.fixture
def sample_flight(sample_uuid):
    return DummyFlight(id=sample_uuid, flight_number="AA123")


@pytest.fixture
def sample_passenger():
    return DummyPassenger(full_name="John Doe", identity_key="DNI-123456")


def test_to_dict_extracts_properties_and_ignores_internal_state(
    sample_flight, sample_uuid
):
    result = sample_flight.to_dict()

    assert "id" in result
    assert "flight_number" in result
    assert result["id"] == sample_uuid
    assert result["flight_number"] == "AA123"

    assert "_id" not in result
    assert "_flight_number" not in result
    assert "_internal_db_state" not in result


def test_to_dict_ignores_identity_key(sample_passenger):
    result = sample_passenger.to_dict()

    assert "full_name" in result
    assert "identity_key" not in result
    assert result["full_name"] == "John Doe"


def test_to_dict_ignores_methods(sample_flight, sample_passenger):
    booking = DummyBooking(
        reference="B-1",
        amount=Decimal("100.00"),
        flight=sample_flight,
        passenger=sample_passenger,
    )

    result = booking.to_dict()

    assert "calculate_tax" not in result
    assert "reference" in result


def test_to_dict_handles_nested_entity_and_ignores_its_identity_key(
    sample_flight, sample_passenger, sample_uuid
):
    booking = DummyBooking(
        reference="B-1",
        amount=Decimal("100.00"),
        flight=sample_flight,
        passenger=sample_passenger,
    )

    result = booking.to_dict()

    assert isinstance(result["flight"], dict)
    assert result["flight"]["flight_number"] == "AA123"

    assert isinstance(result["passenger"], dict)
    assert result["passenger"]["full_name"] == "John Doe"
    assert "identity_key" not in result["passenger"]


def test_to_dict_handles_list_of_nested_entities(sample_uuid, sample_passenger):
    flight_1 = DummyFlight(id=sample_uuid, flight_number="AA123")
    flight_2 = DummyFlight(id=uuid4(), flight_number="BB456")

    booking = DummyBooking(
        reference="B-1",
        amount=Decimal("200.00"),
        flight=flight_1,
        passenger=sample_passenger,
        flights_list=[flight_1, flight_2],
    )

    result = booking.to_dict()

    assert isinstance(result["flights_list"], list)
    assert len(result["flights_list"]) == 2
    assert result["flights_list"][0]["flight_number"] == "AA123"
    assert result["flights_list"][1]["flight_number"] == "BB456"


def test_to_dict_handles_empty_lists(sample_flight, sample_passenger):
    booking = DummyBooking(
        reference="B-1",
        amount=Decimal("100.00"),
        flight=sample_flight,
        passenger=sample_passenger,
        flights_list=[],
    )

    result = booking.to_dict()

    assert "flights_list" in result
    assert result["flights_list"] == []
    assert isinstance(result["flights_list"], list)
