import re
from datetime import datetime
from decimal import Decimal
from typing import cast
from uuid import UUID

import pytest
from factory.declarations import Iterator
from freezegun import freeze_time

from src.api.schemas import BookingRequest, BookingResponse, PassengerRequest
from src.common.exceptions import (
    BlacklistedPassenger,
    FullFlight,
    InexistentFlight,
    MultipleExceptionsError,
    NotScheduledFlight,
    NotSeatsEnough,
)
from src.common.types import BookingDatetime, PaidAmountUsd, PassengerId
from src.core.units_of_work import RegisterBookingUoW
from src.core.use_cases import (
    PassengerProcessor,
    RegisterBooking,
    RegisterBookingValidator,
)
from src.core.validators import BaseValidator, FlightValidator, PassengerValidator
from src.entities import Booking, Document, Flight, Passenger
from tests.factories import (
    DocumentFactory,
    FlightFactory,
    PassengerFactory,
)
from tests.fakes.fake_db_manager import FakeDBManager
from tests.fakes.fake_uows.fake_register_booking_uow import FakeRegisterBookingUoW


def create_register_booking(fake_uow: FakeRegisterBookingUoW) -> RegisterBooking:
    return RegisterBooking(
        uow=cast(RegisterBookingUoW, fake_uow),
        passenger_processor=PassengerProcessor(),
        register_booking_validator=RegisterBookingValidator(
            base_validator=BaseValidator(),
            flight_validator=FlightValidator(),
            passenger_validator=PassengerValidator(),
        ),
    )


def create_passenger_requests(
    passengers_and_documents: list[tuple[Passenger, Document]],
) -> list[PassengerRequest]:
    passenger_requests: list[PassengerRequest] = []
    for passenger_and_document in passengers_and_documents:
        passenger, document = passenger_and_document
        passenger_requests.append(
            PassengerRequest(
                full_name=passenger.full_name,
                birth_date=passenger.birth_date,
                email=passenger.email,
                phone_number=passenger.phone_number,
                document_number=document.document_number,
                valid_from=document.valid_from,
                valid_until=document.valid_until,
                issue_country=document.issue_country,
                document_type_id=document.document_type_id,
            )
        )

    return passenger_requests


def asserts_booking_response(
    booking_response: BookingResponse,
    booking_retrieved: Booking,
    tickets_count_expected: int,
    paid_amount_usd_expected: PaidAmountUsd,
    booking_datetime_expected: BookingDatetime,
) -> None:
    reference_pattern = re.compile(r"^[A-Z0-9]{6}$")

    assert reference_pattern.fullmatch(booking_response.booking_reference) is not None
    assert len(booking_response.tickets) == tickets_count_expected

    for ticket in booking_response.tickets:
        assert len(ticket) == 13 and ticket.isnumeric()

    assert booking_response.booking_datetime == booking_datetime_expected
    assert booking_response.paid_amount_usd == paid_amount_usd_expected

    assert isinstance(booking_retrieved.id, UUID)
    assert booking_retrieved.booking_reference == booking_response.booking_reference
    assert booking_retrieved.booking_datetime == booking_response.booking_datetime
    assert booking_retrieved.paid_amount_usd == booking_response.paid_amount_usd
    assert booking_retrieved.current_status_id == 1


def asserts_repositories(
    uow: FakeRegisterBookingUoW,
    passenger_requests: list[PassengerRequest],
    booking_retrieved: Booking,
) -> None:
    passenger_ids_stored_in_documents: set[PassengerId] = {
        document.passenger_id for document in uow.document_repository.storage.values()
    }

    assert len(passenger_ids_stored_in_documents) == len(passenger_requests)

    for passenger_id in uow.passenger_repository.storage:
        assert passenger_id in passenger_ids_stored_in_documents

    assert uow.booking_repository.storage == {booking_retrieved.id: booking_retrieved}


@freeze_time("2026-01-01 12:00:00")
def test_register_booking_valid_input_existent_passengers() -> None:
    uow = FakeRegisterBookingUoW(FakeDBManager())

    passengers: list[Passenger] = PassengerFactory.build_batch(4)
    documents: list[Document] = DocumentFactory.build_batch(
        4, passenger_id=Iterator([passenger.id for passenger in passengers])
    )

    flight_one: Flight = FlightFactory(base_price_usd=Decimal("1000.00"))
    flight_two: Flight = FlightFactory(base_price_usd=Decimal("2000.00"))

    uow.flight_repository.insert([flight_one, flight_two])
    uow.passenger_repository.insert(passengers)
    uow.document_repository.insert(documents)

    passenger_requests = create_passenger_requests(list(zip(passengers, documents)))

    booking_request = BookingRequest(
        flights_id=[flight_one.id, flight_two.id], passengers=passenger_requests
    )

    register_booking = create_register_booking(fake_uow=uow)

    booking_response: BookingResponse = register_booking.execute(booking_request)

    booking_retrieved: Booking = list(uow.booking_repository.storage.values())[0]

    asserts_booking_response(
        booking_response=booking_response,
        tickets_count_expected=len(passenger_requests) * len([flight_one, flight_two]),
        paid_amount_usd_expected=Decimal("12000.00"),
        booking_datetime_expected=datetime(2026, 1, 1, 12, 0, 0),
        booking_retrieved=booking_retrieved,
    )


@freeze_time("2026-01-01 12:00:00")
def test_register_booking_valid_input_non_existent_passengers() -> None:
    uow = FakeRegisterBookingUoW(FakeDBManager())

    passengers: list[Passenger] = PassengerFactory.build_batch(4)
    documents: list[Document] = DocumentFactory.build_batch(
        4, passenger_id=Iterator([passenger.id for passenger in passengers])
    )

    flight_one: Flight = FlightFactory(base_price_usd=Decimal("1000.00"))
    flight_two: Flight = FlightFactory(base_price_usd=Decimal("2000.00"))

    uow.flight_repository.insert([flight_one, flight_two])

    passenger_requests = create_passenger_requests(list(zip(passengers, documents)))

    booking_request = BookingRequest(
        flights_id=[flight_one.id, flight_two.id], passengers=passenger_requests
    )

    register_booking = create_register_booking(fake_uow=uow)

    booking_response: BookingResponse = register_booking.execute(booking_request)

    booking_retrieved: Booking = list(uow.booking_repository.storage.values())[0]

    asserts_repositories(
        uow=uow,
        passenger_requests=passenger_requests,
        booking_retrieved=booking_retrieved,
    )

    asserts_booking_response(
        booking_response=booking_response,
        tickets_count_expected=len(passenger_requests) * len([flight_one, flight_two]),
        paid_amount_usd_expected=Decimal("12000.00"),
        booking_datetime_expected=datetime(2026, 1, 1, 12, 0, 0),
        booking_retrieved=booking_retrieved,
    )


@freeze_time("2026-01-01 12:00:00")
def test_register_booking_valid_input_existent_and_non_existent_passengers() -> None:
    uow = FakeRegisterBookingUoW(FakeDBManager())

    passengers: list[Passenger] = PassengerFactory.build_batch(4)
    documents: list[Document] = DocumentFactory.build_batch(
        4, passenger_id=Iterator([passenger.id for passenger in passengers])
    )

    flight_one: Flight = FlightFactory(base_price_usd=Decimal("1000.00"))
    flight_two: Flight = FlightFactory(base_price_usd=Decimal("2000.00"))

    passenger_requests = create_passenger_requests(list(zip(passengers, documents)))

    passengers.pop()
    documents.pop()

    uow.flight_repository.insert([flight_one, flight_two])
    uow.passenger_repository.insert(passengers)
    uow.document_repository.insert(documents)

    booking_request = BookingRequest(
        flights_id=[flight_one.id, flight_two.id], passengers=passenger_requests
    )

    register_booking = create_register_booking(fake_uow=uow)

    booking_response: BookingResponse = register_booking.execute(booking_request)

    booking_retrieved: Booking = list(uow.booking_repository.storage.values())[0]

    asserts_repositories(
        uow=uow,
        passenger_requests=passenger_requests,
        booking_retrieved=booking_retrieved,
    )

    asserts_booking_response(
        booking_response=booking_response,
        tickets_count_expected=len(passenger_requests) * len([flight_one, flight_two]),
        paid_amount_usd_expected=Decimal("12000.00"),
        booking_datetime_expected=datetime(2026, 1, 1, 12, 0, 0),
        booking_retrieved=booking_retrieved,
    )


def test_register_booking_inexistent_flights() -> None:
    uow = FakeRegisterBookingUoW(FakeDBManager())

    passengers: list[Passenger] = PassengerFactory.build_batch(4)
    documents: list[Document] = DocumentFactory.build_batch(
        4, passenger_id=Iterator([passenger.id for passenger in passengers])
    )

    flight_one: Flight = FlightFactory(base_price_usd=Decimal("1000.00"))
    flight_two: Flight = FlightFactory(base_price_usd=Decimal("2000.00"))

    uow.passenger_repository.insert(passengers)
    uow.document_repository.insert(documents)

    passenger_requests = create_passenger_requests(list(zip(passengers, documents)))

    booking_request = BookingRequest(
        flights_id=[flight_one.id, flight_two.id], passengers=passenger_requests
    )

    register_booking = create_register_booking(fake_uow=uow)

    with pytest.raises(MultipleExceptionsError) as exc:
        register_booking.execute(booking_request)

    exceptions = {str(exception) for exception in exc.value.exceptions}

    assert exceptions == {
        str(InexistentFlight(flight_one.id)),
        str(InexistentFlight(flight_two.id)),
    }


def test_register_booking_full_flight() -> None:
    uow = FakeRegisterBookingUoW(FakeDBManager())

    passengers: list[Passenger] = PassengerFactory.build_batch(4)
    documents: list[Document] = DocumentFactory.build_batch(
        4, passenger_id=Iterator([passenger.id for passenger in passengers])
    )

    flight_one: Flight = FlightFactory(base_price_usd=Decimal("1000.00"))
    flight_two: Flight = FlightFactory(base_price_usd=Decimal("2000.00"))

    uow.flight_repository.insert([flight_one, flight_two])
    uow.passenger_repository.insert(passengers)
    uow.document_repository.insert(documents)

    uow.flight_repository.seats_available_per_flight[flight_one.id] = 0

    passenger_requests = create_passenger_requests(list(zip(passengers, documents)))

    booking_request = BookingRequest(
        flights_id=[flight_one.id, flight_two.id], passengers=passenger_requests
    )

    register_booking = create_register_booking(fake_uow=uow)

    with pytest.raises(MultipleExceptionsError) as exc:
        register_booking.execute(booking_request)

    exceptions = {str(exception) for exception in exc.value.exceptions}

    assert exceptions == {str(FullFlight(flight_one.id))}


def test_register_booking_not_seats_enough() -> None:
    uow = FakeRegisterBookingUoW(FakeDBManager())

    passengers: list[Passenger] = PassengerFactory.build_batch(4)
    documents: list[Document] = DocumentFactory.build_batch(
        4, passenger_id=Iterator([passenger.id for passenger in passengers])
    )

    flight_one: Flight = FlightFactory(base_price_usd=Decimal("1000.00"))
    flight_two: Flight = FlightFactory(base_price_usd=Decimal("2000.00"))

    uow.flight_repository.insert([flight_one, flight_two])
    uow.passenger_repository.insert(passengers)
    uow.document_repository.insert(documents)

    uow.flight_repository.seats_available_per_flight[flight_one.id] = 100
    uow.flight_repository.seats_available_per_flight[flight_two.id] = 2

    passenger_requests = create_passenger_requests(list(zip(passengers, documents)))

    booking_request = BookingRequest(
        flights_id=[flight_one.id, flight_two.id], passengers=passenger_requests
    )

    register_booking = create_register_booking(fake_uow=uow)

    with pytest.raises(MultipleExceptionsError) as exc:
        register_booking.execute(booking_request)

    exceptions = {str(exception) for exception in exc.value.exceptions}

    assert exceptions == {str(NotSeatsEnough(flight_two.id))}


def test_register_booking_not_scheduled_flight() -> None:
    uow = FakeRegisterBookingUoW(FakeDBManager())

    passengers: list[Passenger] = PassengerFactory.build_batch(4)
    documents: list[Document] = DocumentFactory.build_batch(
        4, passenger_id=Iterator([passenger.id for passenger in passengers])
    )

    flight_one: Flight = FlightFactory(
        base_price_usd=Decimal("1000.00"), current_status_id=2
    )
    flight_two: Flight = FlightFactory(base_price_usd=Decimal("2000.00"))

    uow.flight_repository.insert([flight_one, flight_two])
    uow.passenger_repository.insert(passengers)
    uow.document_repository.insert(documents)

    passenger_requests = create_passenger_requests(list(zip(passengers, documents)))

    booking_request = BookingRequest(
        flights_id=[flight_one.id, flight_two.id], passengers=passenger_requests
    )

    register_booking = create_register_booking(fake_uow=uow)

    with pytest.raises(MultipleExceptionsError) as exc:
        register_booking.execute(booking_request)

    exceptions = {str(exception) for exception in exc.value.exceptions}

    assert exceptions == {str(NotScheduledFlight(flight_one.id))}


def test_register_booking_blacklisted_passenger() -> None:
    uow = FakeRegisterBookingUoW(FakeDBManager())

    passengers: list[Passenger] = PassengerFactory.build_batch(
        4, is_blacklisted=Iterator([True, False, False, False])
    )
    documents: list[Document] = DocumentFactory.build_batch(
        4, passenger_id=Iterator([passenger.id for passenger in passengers])
    )

    flight_one: Flight = FlightFactory(base_price_usd=Decimal("1000.00"))
    flight_two: Flight = FlightFactory(base_price_usd=Decimal("2000.00"))

    uow.flight_repository.insert([flight_one, flight_two])
    uow.passenger_repository.insert(passengers)
    uow.document_repository.insert(documents)

    passenger_requests = create_passenger_requests(list(zip(passengers, documents)))

    booking_request = BookingRequest(
        flights_id=[flight_one.id, flight_two.id], passengers=passenger_requests
    )

    register_booking = create_register_booking(fake_uow=uow)

    with pytest.raises(MultipleExceptionsError) as exc:
        register_booking.execute(booking_request)

    exceptions = {str(exception) for exception in exc.value.exceptions}

    assert exceptions == {str(BlacklistedPassenger(passengers[0].id))}


def test_register_booking_multiple_exceptions() -> None:
    uow = FakeRegisterBookingUoW(FakeDBManager())

    passengers: list[Passenger] = PassengerFactory.build_batch(
        4, is_blacklisted=Iterator([True, False, False, False])
    )
    documents: list[Document] = DocumentFactory.build_batch(
        4, passenger_id=Iterator([passenger.id for passenger in passengers])
    )

    flight_one: Flight = FlightFactory(
        base_price_usd=Decimal("1000.00"), current_status_id=2
    )
    flight_two: Flight = FlightFactory(base_price_usd=Decimal("2000.00"))

    uow.flight_repository.insert([flight_one, flight_two])
    uow.passenger_repository.insert(passengers)
    uow.document_repository.insert(documents)

    uow.flight_repository.seats_available_per_flight[flight_two.id] = 0

    passenger_requests = create_passenger_requests(list(zip(passengers, documents)))

    booking_request = BookingRequest(
        flights_id=[flight_one.id, flight_two.id], passengers=passenger_requests
    )

    register_booking = create_register_booking(fake_uow=uow)

    with pytest.raises(MultipleExceptionsError) as exc:
        register_booking.execute(booking_request)

    exceptions = {str(exception) for exception in exc.value.exceptions}

    assert exceptions == {
        str(FullFlight(flight_two.id)),
        str(NotScheduledFlight(flight_one.id)),
        str(BlacklistedPassenger(passengers[0].id)),
    }


def test_register_booking_multiple_exceptions_same_exceptions() -> None:
    uow = FakeRegisterBookingUoW(FakeDBManager())

    passengers: list[Passenger] = PassengerFactory.build_batch(
        4, is_blacklisted=Iterator([True, True, True, True])
    )
    documents: list[Document] = DocumentFactory.build_batch(
        4, passenger_id=Iterator([passenger.id for passenger in passengers])
    )

    flight_one: Flight = FlightFactory(
        base_price_usd=Decimal("1000.00"), current_status_id=2
    )
    flight_two: Flight = FlightFactory(base_price_usd=Decimal("2000.00"))

    uow.flight_repository.insert([flight_one, flight_two])
    uow.passenger_repository.insert(passengers)
    uow.document_repository.insert(documents)

    uow.flight_repository.seats_available_per_flight[flight_two.id] = 0

    passenger_requests = create_passenger_requests(list(zip(passengers, documents)))

    booking_request = BookingRequest(
        flights_id=[flight_one.id, flight_two.id], passengers=passenger_requests
    )

    register_booking = create_register_booking(fake_uow=uow)

    with pytest.raises(MultipleExceptionsError) as exc:
        register_booking.execute(booking_request)

    exceptions = {str(exception) for exception in exc.value.exceptions}

    blacklisted_passenger_exceptions = {
        str(BlacklistedPassenger(passenger.id)) for passenger in passengers
    }

    assert exceptions == {
        str(FullFlight(flight_two.id)),
        str(NotScheduledFlight(flight_one.id)),
    }.union(blacklisted_passenger_exceptions)
