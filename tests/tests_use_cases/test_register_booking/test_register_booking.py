from collections.abc import Sequence
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import cast

import pytest
from freezegun import freeze_time

from src.api.schemas import BookingRequest, BookingResponse
from src.common.exceptions import (BlacklistedPassenger, FullFlight,
                                    InexistentFlight, InvalidData,
                                    MultipleExceptionsError, NotScheduledFlight,
                                    NotSeatsEnough)
from src.common.types import BookingId, BookingReference, TicketNumber
from src.core.units_of_work import RegisterBookingUoW
from src.core.use_cases import (PassengerProcessor, RegisterBooking,
                                RegisterBookingValidator)
from src.core.validators import (BaseValidator, FlightValidator,
                                PassengerValidator)
from src.entities import Booking, Document, Flight, Passenger, Ticket
from tests.fakes.fake_db_manager import FakeDBManager
from tests.fakes.fake_uows.fake_register_booking_uow import \
    FakeRegisterBookingUoW


def calculate_paid_amount_usd(
    flights_created: list[Flight], number_of_passengers: int
) -> Decimal:
    return (
        sum((flight.base_price_usd for flight in flights_created), Decimal("0"))
        * number_of_passengers
    ).quantize(Decimal("0.01"), ROUND_HALF_UP)


def calculate_base_price_usd(operating_cost_usd: Decimal) -> Decimal:
    return (operating_cost_usd * Decimal("1.30")).quantize(
        Decimal("0.01"), ROUND_HALF_UP
    )


def create_register_booking(fake_uow: FakeRegisterBookingUoW) -> RegisterBooking:
    return RegisterBooking(
        uow=cast(RegisterBookingUoW, fake_uow),
        passenger_processor=PassengerProcessor(),
        register_booking_validator=RegisterBookingValidator(
            BaseValidator(), FlightValidator(), PassengerValidator()
        ),
    )


def asserts(
    fake_uow: FakeRegisterBookingUoW,
    booking_request: BookingRequest,
    booking_response: BookingResponse,
    documents_generated: list[Document],
    flights_generated: list[Flight],
    passengers_generated: list[Passenger],
    tickets_generated: list[Ticket],
    expected_booking_reference: BookingReference,
    expected_ticket_number: TicketNumber,
    expected_booking_id: BookingId,
) -> None:
    booking_expected = Booking.new_booking(
        [flight.base_price_usd for flight in flights_generated],
        len(booking_request.passengers),
    )
    booking_expected.id = expected_booking_id

    assert fake_uow.booking_repository.bookings == [booking_expected]
    assert fake_uow.document_repository.documents == documents_generated
    assert fake_uow.passenger_repository.passengers == passengers_generated
    assert fake_uow.ticket_repository.tickets == tickets_generated

    expected_tickets_count = len(booking_request.passengers) * len(
        booking_request.flights_id
    )

    assert booking_response.booking_reference == expected_booking_reference
    assert booking_response.tickets == [expected_ticket_number] * expected_tickets_count
    assert isinstance(booking_response.booking_datetime, datetime)
    assert booking_response.paid_amount_usd == calculate_paid_amount_usd(
        flights_generated, len(booking_request.passengers)
    )


@freeze_time("2026-01-01 12:00:00")
@pytest.mark.usefixtures("fixed_booking_identifiers")
def test_register_booking_valid_input_existent_passengers(
    booking_request: BookingRequest,
    passengers_and_documents_generated: tuple[list[Passenger], list[Document]],
    flights_generated: list[Flight],
    tickets_generated: list[Ticket],
    expected_booking_reference: BookingReference,
    expected_ticket_number: TicketNumber,
    expected_booking_id: BookingId,
) -> None:
    fake_uow = FakeRegisterBookingUoW(FakeDBManager())
    passengers_generated, documents_generated = passengers_and_documents_generated

    fake_uow.document_repository.insert_documents(documents_generated)
    fake_uow.flight_repository.insert_flights(flights_generated)
    fake_uow.passenger_repository.insert_passengers(passengers_generated)

    register_booking: RegisterBooking = create_register_booking(fake_uow)
    booking_response: BookingResponse = register_booking.execute(booking_request)

    asserts(
        fake_uow,
        booking_request,
        booking_response,
        documents_generated,
        flights_generated,
        passengers_generated,
        tickets_generated,
        expected_booking_reference,
        expected_ticket_number,
        expected_booking_id,
    )


@freeze_time("2026-01-01 12:00:00")
@pytest.mark.usefixtures("fixed_booking_identifiers")
def test_register_booking_valid_input_non_existent_passengers(
    booking_request: BookingRequest,
    passengers_and_documents_generated: tuple[list[Passenger], list[Document]],
    flights_generated: list[Flight],
    tickets_generated: list[Ticket],
    expected_booking_reference: BookingReference,
    expected_ticket_number: TicketNumber,
    expected_booking_id: BookingId,
) -> None:
    passengers_generated, documents_generated = passengers_and_documents_generated
    fake_uow = FakeRegisterBookingUoW(FakeDBManager())

    fake_uow.flight_repository.insert_flights(flights_generated)

    register_booking: RegisterBooking = create_register_booking(fake_uow)
    booking_response: BookingResponse = register_booking.execute(booking_request)

    asserts(
        fake_uow,
        booking_request,
        booking_response,
        documents_generated,
        flights_generated,
        passengers_generated,
        tickets_generated,
        expected_booking_reference,
        expected_ticket_number,
        expected_booking_id,
    )


@freeze_time("2026-01-01 12:00:00")
@pytest.mark.usefixtures("fixed_booking_identifiers")
def test_register_booking_valid_input_existent_and_non_existent_passengers(
    booking_request: BookingRequest,
    passengers_and_documents_generated: tuple[list[Passenger], list[Document]],
    flights_generated: list[Flight],
    tickets_generated: list[Ticket],
    expected_booking_reference: BookingReference,
    expected_ticket_number: TicketNumber,
    expected_booking_id: BookingId,
) -> None:
    passengers_generated, documents_generated = passengers_and_documents_generated
    fake_uow = FakeRegisterBookingUoW(FakeDBManager())

    fake_uow.flight_repository.insert_flights(flights_generated)
    fake_uow.passenger_repository.insert_passengers([passengers_generated[0]])
    fake_uow.document_repository.insert_documents([documents_generated[0]])

    register_booking: RegisterBooking = create_register_booking(fake_uow)
    booking_response: BookingResponse = register_booking.execute(booking_request)

    asserts(
        fake_uow,
        booking_request,
        booking_response,
        documents_generated,
        flights_generated,
        passengers_generated,
        tickets_generated,
        expected_booking_reference,
        expected_ticket_number,
        expected_booking_id,
    )


def test_register_booking_inexistent_flights(booking_request: BookingRequest) -> None:
    fake_uow = FakeRegisterBookingUoW(FakeDBManager())

    register_booking: RegisterBooking = create_register_booking(fake_uow)

    with pytest.raises(MultipleExceptionsError) as exc_info:
        register_booking.execute(booking_request)

    exceptions: Sequence[InvalidData] = exc_info.value.exceptions

    assert len(exceptions) == 2
    assert isinstance(exceptions[0], InexistentFlight)
    assert isinstance(exceptions[0], InexistentFlight)


def test_register_booking_full_flight(
    booking_request: BookingRequest, flights_generated: list[Flight]
) -> None:
    fake_uow = FakeRegisterBookingUoW(FakeDBManager())

    fake_uow.flight_repository.insert_flights(flights_generated)

    fake_uow.flight_repository.flights[flights_generated[0]] = 0

    register_booking: RegisterBooking = create_register_booking(fake_uow)

    with pytest.raises(MultipleExceptionsError) as exc_info:
        register_booking.execute(booking_request)

    exceptions: Sequence[InvalidData] = exc_info.value.exceptions

    assert len(exceptions) == 1
    assert isinstance(exceptions[0], FullFlight)


def test_register_booking_not_seats_enough(
    booking_request: BookingRequest, flights_generated: list[Flight]
) -> None:
    fake_uow = FakeRegisterBookingUoW(FakeDBManager())

    fake_uow.flight_repository.insert_flights(flights_generated, seats=1)

    register_booking: RegisterBooking = create_register_booking(fake_uow)

    with pytest.raises(MultipleExceptionsError) as exc_info:
        register_booking.execute(booking_request)

    exceptions: Sequence[InvalidData] = exc_info.value.exceptions

    assert len(exceptions) == 2
    assert isinstance(exceptions[0], NotSeatsEnough)
    assert isinstance(exceptions[1], NotSeatsEnough)


def test_register_booking_not_scheduled_flight(
    booking_request: BookingRequest, flights_generated: list[Flight]
) -> None:
    fake_uow = FakeRegisterBookingUoW(FakeDBManager())

    flights_generated[0].current_status_id = 99

    fake_uow.flight_repository.insert_flights(flights_generated)

    register_booking: RegisterBooking = create_register_booking(fake_uow)

    with pytest.raises(MultipleExceptionsError) as exc_info:
        register_booking.execute(booking_request)

    exceptions: Sequence[InvalidData] = exc_info.value.exceptions

    assert len(exceptions) == 1
    assert isinstance(exceptions[0], NotScheduledFlight)


def test_register_booking_blacklisted_passenger(
    booking_request: BookingRequest,
    flights_generated: list[Flight],
    passengers_generated: list[Passenger],
) -> None:
    fake_uow = FakeRegisterBookingUoW(FakeDBManager())

    passengers_generated[0].is_blacklisted = True

    fake_uow.flight_repository.insert_flights(flights_generated)
    fake_uow.passenger_repository.insert_passengers(passengers_generated)

    register_booking: RegisterBooking = create_register_booking(fake_uow)

    with pytest.raises(MultipleExceptionsError) as exc_info:
        register_booking.execute(booking_request)

    exceptions: Sequence[InvalidData] = exc_info.value.exceptions

    assert len(exceptions) == 1
    assert isinstance(exceptions[0], BlacklistedPassenger)


def test_register_booking_multiple_exceptions(
    booking_request: BookingRequest,
    flights_generated: list[Flight],
    passengers_generated: list[Passenger],
) -> None:
    fake_uow = FakeRegisterBookingUoW(FakeDBManager())

    passengers_generated[0].is_blacklisted = True
    flights_generated[0].current_status_id = 99

    fake_uow.flight_repository.insert_flights(flights_generated)
    fake_uow.passenger_repository.insert_passengers(passengers_generated)

    fake_uow.flight_repository.flights[flights_generated[0]] = 0

    register_booking: RegisterBooking = create_register_booking(fake_uow)

    with pytest.raises(MultipleExceptionsError) as exc_info:
        register_booking.execute(booking_request)

    exceptions: Sequence[InvalidData] = exc_info.value.exceptions

    assert len(exceptions) == 3
    assert isinstance(exceptions[0], FullFlight)
    assert isinstance(exceptions[1], NotScheduledFlight)
    assert isinstance(exceptions[2], BlacklistedPassenger)
