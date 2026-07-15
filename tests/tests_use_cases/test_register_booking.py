from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from freezegun import freeze_time
import pytest
from typing import cast

from src.api.schemas import BookingRequest, BookingResponse
from src.common.exceptions import InexistentFlight
from src.common.types import BookingId, BookingReference, TicketNumber
from src.core.units_of_work import CreateBookingUoW
from src.core.use_cases import RegisterBooking, CreateBookingValidator, PassengerProcessor
from src.core.validators import BaseValidator, FlightValidator, PassengerValidator
from src.entities import Booking, Document, Flight, Passenger, Ticket
from tests.fakes.fake_uows.fake_create_booking_uow import FakeCreateBookingUoW
from tests.fakes.fake_db_manager import FakeDBManager

def calculate_paid_amount_usd(flights_created: list[Flight], number_of_passengers: int) -> Decimal:
    return (sum((flight.base_price_usd for flight in flights_created), Decimal("0")) * number_of_passengers).quantize(Decimal("0.01"), ROUND_HALF_UP)

def calculate_base_price_usd(operating_cost_usd: Decimal) -> Decimal:
        return (operating_cost_usd * Decimal("1.30")).quantize(Decimal("0.01"), ROUND_HALF_UP)

def create_register_booking(fake_uow: FakeCreateBookingUoW) -> RegisterBooking:
    return RegisterBooking(
        uow=cast(CreateBookingUoW, fake_uow),
        passenger_processor=PassengerProcessor(),
        create_booking_validator=CreateBookingValidator(BaseValidator(), FlightValidator(), PassengerValidator())
    )

def asserts(fake_uow: FakeCreateBookingUoW, booking_request: BookingRequest, booking_response: BookingResponse, documents_generated: list[Document], 
            flights_generated: list[Flight], passengers_generated: list[Passenger],  tickets_generated: list[Ticket], expected_booking_reference: BookingReference,
            expected_ticket_number: TicketNumber, expected_booking_id: BookingId):
    booking_expected = Booking.new_booking([flight.base_price_usd for flight in flights_generated], len(booking_request.passengers))
    booking_expected.id = expected_booking_id
    
    assert fake_uow.booking_repository.bookings == [booking_expected]
    assert fake_uow.document_repository.documents == documents_generated
    assert fake_uow.passenger_repository.passengers == passengers_generated
    assert fake_uow.ticket_repository.tickets == tickets_generated

    expected_tickets_count = len(booking_request.passengers) * len(booking_request.flights_id)

    assert booking_response.booking_reference == expected_booking_reference
    assert booking_response.tickets == [expected_ticket_number] * expected_tickets_count
    assert isinstance(booking_response.booking_datetime, datetime)
    assert booking_response.paid_amount_usd == calculate_paid_amount_usd(flights_generated, len(booking_request.passengers))

@freeze_time("2026-01-01 12:00:00")
@pytest.mark.usefixtures("fixed_booking_identifiers")
def test_create_booking_valid_input_existent_passengers(booking_request: BookingRequest, passengers_and_documents_generated: tuple[list[Passenger], list[Document]],
                                                        flights_generated: list[Flight], tickets_generated: list[Ticket], expected_booking_reference: BookingReference,
                                                        expected_ticket_number: TicketNumber, expected_booking_id: BookingId) -> None:
    fake_uow = FakeCreateBookingUoW(FakeDBManager())
    passengers_generated, documents_generated = passengers_and_documents_generated

    fake_uow.document_repository.insert_documents(documents_generated)
    fake_uow.flight_repository.insert_flights(flights_generated)
    fake_uow.passenger_repository.insert_passengers(passengers_generated)

    register_booking: RegisterBooking = create_register_booking(fake_uow)
    booking_response: BookingResponse = register_booking.execute(booking_request)

    asserts(fake_uow, booking_request, booking_response, documents_generated, flights_generated, 
            passengers_generated, tickets_generated, expected_booking_reference, expected_ticket_number, expected_booking_id)

@freeze_time("2026-01-01 12:00:00")
@pytest.mark.usefixtures("fixed_booking_identifiers")
def test_create_booking_valid_input_non_existent_passengers(booking_request: BookingRequest,  passengers_and_documents_generated: tuple[list[Passenger], list[Document]],
                                                            flights_generated: list[Flight], tickets_generated: list[Ticket], expected_booking_reference: BookingReference,
                                                            expected_ticket_number: TicketNumber, expected_booking_id: BookingId) -> None:
    passengers_generated, documents_generated = passengers_and_documents_generated
    fake_uow = FakeCreateBookingUoW(FakeDBManager())

    fake_uow.flight_repository.insert_flights(flights_generated)

    register_booking: RegisterBooking = create_register_booking(fake_uow)
    booking_response: BookingResponse = register_booking.execute(booking_request)

    asserts(fake_uow, booking_request, booking_response, documents_generated, flights_generated, 
            passengers_generated, tickets_generated, expected_booking_reference, expected_ticket_number, expected_booking_id)

@freeze_time("2026-01-01 12:00:00")
@pytest.mark.usefixtures("fixed_booking_identifiers")
def test_create_booking_valid_input_existent_and_non_existent_passengers(booking_request: BookingRequest,  passengers_and_documents_generated: tuple[list[Passenger], list[Document]],
                                                            flights_generated: list[Flight], tickets_generated: list[Ticket], expected_booking_reference: BookingReference,
                                                            expected_ticket_number: TicketNumber, expected_booking_id: BookingId) -> None:
    passengers_generated, documents_generated = passengers_and_documents_generated
    fake_uow = FakeCreateBookingUoW(FakeDBManager())

    fake_uow.flight_repository.insert_flights(flights_generated)
    fake_uow.passenger_repository.insert_passengers([passengers_generated[0]])
    fake_uow.document_repository.insert_documents([documents_generated[0]])

    register_booking: RegisterBooking = create_register_booking(fake_uow)
    booking_response: BookingResponse = register_booking.execute(booking_request)

    asserts(fake_uow, booking_request, booking_response, documents_generated, flights_generated, 
            passengers_generated, tickets_generated, expected_booking_reference, expected_ticket_number, expected_booking_id)

def test_create_booking_inexistent_flight(booking_request: BookingRequest) -> None:
    fake_uow = FakeCreateBookingUoW(FakeDBManager())
    
    register_booking: RegisterBooking = create_register_booking(fake_uow)

    with pytest.raises(InexistentFlight):
        register_booking.execute(booking_request)

def test_create_booking_full_flight() -> None:
    pass

def test_create_booking_not_scheduled_flight() -> None:
    pass

def test_create_booking_blacklisted_passenger() -> None:
    pass

def test_create_booking_multiple_exceptions() -> None:
    pass