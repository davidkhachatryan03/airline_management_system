from typing import cast
from collections.abc import Sequence

import pytest

from src.api.schemas import FlightRequest, FlightResponse
from src.common.exceptions import (
    DuplicatedFlight,
    InexistentAirplane,
    InexistentRoute,
    InvalidData,
    MultipleExceptionsError,
    UnavailableAirplane,
)
from src.common.types import FlightId
from src.core.units_of_work import RegisterFlightUoW
from src.core.use_cases import RegisterFlight, RegisterFlightValidator
from src.core.validators import BaseValidator, FlightValidator
from src.entities import Airplane, Flight, Route
from tests.fakes.fake_db_manager import FakeDBManager
from tests.fakes.fake_uows.fake_register_flight_uow import FakeRegisterFlightUoW


def create_register_flight(fake_uow: FakeRegisterFlightUoW) -> RegisterFlight:
    return RegisterFlight(
        uow=cast(RegisterFlightUoW, fake_uow),
        register_flight_validator=RegisterFlightValidator(
            BaseValidator(), FlightValidator()
        ),
    )


@pytest.mark.usefixtures("fixed_flight_identifiers")
def test_register_flight_valid_input(
    flight_request: FlightRequest,
    route_generated: Route,
    airplane_generated: Airplane,
    expected_flight_id: FlightId,
) -> None:
    fake_uow = FakeRegisterFlightUoW(FakeDBManager())

    fake_uow.airplane_repository.insert_airplanes([airplane_generated])
    fake_uow.route_repository.insert_routes([route_generated])

    register_flight: RegisterFlight = create_register_flight(fake_uow)
    flight_response: FlightResponse = register_flight.execute(flight_request)

    flight_expected = Flight.new_flight(
        scheduled_departure_datetime=flight_request.scheduled_departure_datetime,
        scheduled_arrival_datetime=flight_request.scheduled_arrival_datetime,
        operating_cost_usd=Flight._calculate_operating_cost_usd(
            airplane_generated.flight_hour_cost_usd, route_generated.duration_min
        ),
        route_id=route_generated.id,
        airplane_id=airplane_generated.id,
    )
    flight_expected.id = expected_flight_id

    assert len(fake_uow.flight_repository.flights) == 1
    assert list(fake_uow.flight_repository.flights.keys()) == [flight_expected]

    assert flight_response.id == expected_flight_id


def test_register_flight_inexistent_airplane(
    flight_request: FlightRequest, route_generated: Route
) -> None:
    fake_uow = FakeRegisterFlightUoW(FakeDBManager())

    fake_uow.route_repository.insert_routes([route_generated])

    register_flight: RegisterFlight = create_register_flight(fake_uow)

    with pytest.raises(MultipleExceptionsError) as exc_info:
        register_flight.execute(flight_request)

    exceptions: Sequence[InvalidData] = exc_info.value.exceptions

    assert len(exceptions) == 1
    assert isinstance(exceptions[0], InexistentAirplane)


def test_register_flight_unavailable_airplane(
    flight_request: FlightRequest,
    route_generated: Route,
    unavailable_airplane: Airplane,
) -> None:
    fake_uow = FakeRegisterFlightUoW(FakeDBManager())

    fake_uow.airplane_repository.insert_airplanes([unavailable_airplane])
    fake_uow.route_repository.insert_routes([route_generated])

    flight_request.airplane_id = unavailable_airplane.id

    register_flight: RegisterFlight = create_register_flight(fake_uow)

    with pytest.raises(MultipleExceptionsError) as exc_info:
        register_flight.execute(flight_request)

    exceptions: Sequence[InvalidData] = exc_info.value.exceptions

    assert len(exceptions) == 1
    assert isinstance(exceptions[0], UnavailableAirplane)


def test_register_flight_inexistent_route(
    flight_request: FlightRequest, airplane_generated: Airplane
) -> None:
    fake_uow = FakeRegisterFlightUoW(FakeDBManager())

    fake_uow.airplane_repository.insert_airplanes([airplane_generated])

    register_flight: RegisterFlight = create_register_flight(fake_uow)

    with pytest.raises(MultipleExceptionsError) as exc_info:
        register_flight.execute(flight_request)

    exceptions: Sequence[InvalidData] = exc_info.value.exceptions

    assert len(exceptions) == 1
    assert isinstance(exceptions[0], InexistentRoute)


def test_register_flight_duplicated_flight(
    flight_request: FlightRequest,
    flight_generated: Flight,
    route_generated: Route,
    airplane_generated: Airplane,
) -> None:
    fake_uow = FakeRegisterFlightUoW(FakeDBManager())

    fake_uow.airplane_repository.insert_airplanes([airplane_generated])
    fake_uow.route_repository.insert_routes([route_generated])
    fake_uow.flight_repository.insert_flights([flight_generated])

    register_flight: RegisterFlight = create_register_flight(fake_uow)

    with pytest.raises(MultipleExceptionsError) as exc_info:
        register_flight.execute(flight_request)

    exceptions: Sequence[InvalidData] = exc_info.value.exceptions

    assert len(exceptions) == 1
    assert isinstance(exceptions[0], DuplicatedFlight)
