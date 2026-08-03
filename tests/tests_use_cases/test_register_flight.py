import re
from datetime import datetime
from decimal import Decimal
from typing import cast
from uuid import UUID

import pytest
from factory.declarations import Iterator
from freezegun import freeze_time

from src.api.schemas import FlightRequest, FlightResponse
from src.common.exceptions import (
    DuplicatedFlight,
    InexistentAirplane,
    InexistentRoute,
    MultipleExceptionsError,
    UnavailableAirplane,
)
from src.common.types import BookingDatetime, PaidAmountUsd, PassengerId
from src.core.units_of_work import RegisterFlightUoW
from src.core.use_cases import RegisterFlight, RegisterFlightValidator
from src.core.validators import BaseValidator, FlightValidator, PassengerValidator
from src.entities import Airplane, Booking, Document, Flight, Passenger, Route
from tests.factories import AirplaneFactory, FlightFactory, RouteFactory
from tests.fakes.fake_db_manager import FakeDBManager
from tests.fakes.fake_uows.fake_register_flight_uow import FakeRegisterFlightUoW


def create_register_flight(fake_uow: FakeRegisterFlightUoW) -> RegisterFlight:
    return RegisterFlight(
        uow=cast(RegisterFlightUoW, fake_uow),
        register_flight_validator=RegisterFlightValidator(
            base_validator=BaseValidator(), flight_validator=FlightValidator()
        ),
    )


def test_register_flight_valid_input() -> None:
    uow = FakeRegisterFlightUoW(FakeDBManager())

    flight: Flight = FlightFactory()
    airplane: Airplane = AirplaneFactory()
    route: Route = RouteFactory()

    flight_request = FlightRequest(
        scheduled_departure_datetime=flight.scheduled_departure_datetime,
        scheduled_arrival_datetime=flight.scheduled_arrival_datetime,
        route_id=flight.route_id,
        airplane_id=flight.airplane_id,
    )

    uow.airplane_repository.insert([airplane])
    uow.route_repository.insert([route])

    register_flight: RegisterFlight = create_register_flight(uow)

    flight_response: FlightResponse = register_flight.execute(flight_request)

    assert isinstance(flight_response.id, UUID)

    flight_retrieved: Flight = list(uow.flight_repository.storage.values())[0]

    assert isinstance(flight_retrieved.id, UUID)
    assert uow.flight_repository.storage == {flight_retrieved.id: flight_retrieved}


def test_register_flight_inexistent_airplane() -> None:
    uow = FakeRegisterFlightUoW(FakeDBManager())

    flight: Flight = FlightFactory()
    route: Route = RouteFactory()

    flight_request = FlightRequest(
        scheduled_departure_datetime=flight.scheduled_departure_datetime,
        scheduled_arrival_datetime=flight.scheduled_arrival_datetime,
        route_id=flight.route_id,
        airplane_id=flight.airplane_id,
    )

    uow.route_repository.insert([route])

    register_flight: RegisterFlight = create_register_flight(uow)

    with pytest.raises(MultipleExceptionsError) as exc:
        register_flight.execute(flight_request)

    exceptions = {str(exception) for exception in exc.value.exceptions}

    assert set(exceptions) == {str(InexistentAirplane(flight_request.airplane_id))}


def test_register_flight_unavailable_airplane() -> None:
    uow = FakeRegisterFlightUoW(FakeDBManager())

    flight: Flight = FlightFactory()
    airplane: Airplane = AirplaneFactory(range_km=1)
    route: Route = RouteFactory()

    flight_request = FlightRequest(
        scheduled_departure_datetime=flight.scheduled_departure_datetime,
        scheduled_arrival_datetime=flight.scheduled_arrival_datetime,
        route_id=flight.route_id,
        airplane_id=flight.airplane_id,
    )

    uow.airplane_repository.insert([airplane])
    uow.route_repository.insert([route])

    register_flight: RegisterFlight = create_register_flight(uow)

    with pytest.raises(MultipleExceptionsError) as exc:
        register_flight.execute(flight_request)

    exceptions = {str(exception) for exception in exc.value.exceptions}

    assert exceptions == {str(UnavailableAirplane(flight_request.airplane_id))}


def test_register_flight_inexistent_route() -> None:
    uow = FakeRegisterFlightUoW(FakeDBManager())

    flight: Flight = FlightFactory()
    airplane: Airplane = AirplaneFactory()

    flight_request = FlightRequest(
        scheduled_departure_datetime=flight.scheduled_departure_datetime,
        scheduled_arrival_datetime=flight.scheduled_arrival_datetime,
        route_id=flight.route_id,
        airplane_id=flight.airplane_id,
    )

    uow.airplane_repository.insert([airplane])

    register_flight: RegisterFlight = create_register_flight(uow)

    with pytest.raises(MultipleExceptionsError) as exc:
        register_flight.execute(flight_request)

    exceptions = {str(exception) for exception in exc.value.exceptions}

    assert exceptions == {str(InexistentRoute(flight_request.route_id))}


def test_register_flight_duplicated_flight() -> None:
    uow = FakeRegisterFlightUoW(FakeDBManager())

    flight: Flight = FlightFactory()
    airplane: Airplane = AirplaneFactory()
    route: Route = RouteFactory()

    flight_request = FlightRequest(
        scheduled_departure_datetime=flight.scheduled_departure_datetime,
        scheduled_arrival_datetime=flight.scheduled_arrival_datetime,
        route_id=flight.route_id,
        airplane_id=flight.airplane_id,
    )

    uow.flight_repository.insert([flight])
    uow.airplane_repository.insert([airplane])
    uow.route_repository.insert([route])

    register_flight: RegisterFlight = create_register_flight(uow)

    with pytest.raises(MultipleExceptionsError) as exc:
        register_flight.execute(flight_request)

    exceptions = {str(exception) for exception in exc.value.exceptions}

    assert exceptions == {str(DuplicatedFlight(flight.identity_key))}
