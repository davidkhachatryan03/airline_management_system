from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

import pytest
from pytest_mock import MockerFixture

from src.api.schemas import BookingRequest, PassengerRequest
from src.common.types import (BookingId, BookingReference, FlightId,
                              TicketNumber)
from src.entities import Document, Flight, Passenger, Ticket


@pytest.fixture
def booking_request() -> BookingRequest:
    return BookingRequest(
        flights_id=[UUID("019f60a9-c89e-7138-b9c4-3e554055cee0"), UUID("019f60aa-338d-799b-9f43-134050b58020")],
        passengers=[
            PassengerRequest(
            full_name="David Khachatryan",
            birth_date=date(2000,1,1),
            email="example@mail.com",
            phone_number="123456789",
            document_number="1122334455",
            valid_from=date(2020,1,1),
            valid_until=date(2030,1,1),
            issue_country="ARG",
            document_type_id=1
            ),
            PassengerRequest(
            full_name="John Doe",
            birth_date=date(2000,1,1),
            email="example@mail.com",
            phone_number="123456789",
            document_number="987654321",
            valid_from=date(2020,1,1),
            valid_until=date(2030,1,1),
            issue_country="USA",
            document_type_id=1
            )
        ])

@pytest.fixture
def flights_generated(booking_request: BookingRequest) -> list[Flight]:
    flights_generated: list[Flight] = []

    flights_ids: list[FlightId] = booking_request.flights_id
    for flight_id in flights_ids:
        flight_generated = Flight.new_flight(
            scheduled_departure_datetime=datetime(2020,3, 3),
            scheduled_arrival_datetime=datetime(2020, 3, 4),
            operating_cost_usd=Decimal("7000"),
            route_id=1,
            airplane_id=1
        )
        flight_generated.id = flight_id

        flights_generated.append(flight_generated)
    
    return flights_generated

@pytest.fixture
def passengers_and_documents_generated(booking_request: BookingRequest) -> tuple[list[Passenger], list[Document]]:
    passengers_generated: list[Passenger] = []
    documents_generated: list[Document] = []
    passenger_requested: list[PassengerRequest] = booking_request.passengers

    for passenger in passenger_requested:
        passenger_generated = Passenger.new_passenger(
            full_name=passenger.full_name,
            birth_date=passenger.birth_date,
            email=passenger.email,
            phone_number=passenger.phone_number
        )

        document_generated = Document.new_document(
            document_number=passenger.document_number,
            valid_from=passenger.valid_from,
            valid_until=passenger.valid_until,
            issue_country=passenger.issue_country,
            passenger_id=passenger_generated.id,
            document_type_id=passenger.document_type_id
        )

        passengers_generated.append(passenger_generated)
        documents_generated.append(document_generated)
    
    return passengers_generated, documents_generated

@pytest.fixture
def passengers_generated(passengers_and_documents_generated: tuple[list[Passenger], list[Document]]) -> list[Passenger]:
    return passengers_and_documents_generated[0]

@pytest.fixture
def documents_generated(passengers_and_documents_generated: tuple[list[Passenger], list[Document]]) -> list[Document]:
    return passengers_and_documents_generated[1]

@pytest.fixture
def tickets_generated(passengers_generated: list[Passenger],
                    flights_generated: list[Flight],
                    expected_booking_id: UUID,
                    expected_ticket_number: str) -> list[Ticket]:
    tickets_generated: list[Ticket] = []

    for passenger in passengers_generated:
        for flight in flights_generated:
            ticket_generated = Ticket.new_ticket(
                paid_amount_usd=flight.base_price_usd,
                booking_id=expected_booking_id,
                flight_id=flight.id,
                passenger_id=passenger.id
            )
            ticket_generated.ticket_number = expected_ticket_number

            tickets_generated.append(ticket_generated)

    return tickets_generated

@pytest.fixture
def fixed_booking_identifiers(mocker: MockerFixture, expected_booking_id: BookingId, expected_booking_reference: BookingReference, expected_ticket_number: TicketNumber):

    mocker.patch(
        "src.entities.booking.uuid6.uuid7", 
        return_value=expected_booking_id
    )

    mocker.patch(
        "src.entities.Booking._generate_reference",
        return_value=expected_booking_reference
    )

    mocker.patch(
        "src.entities.Ticket._generate_ticket_number",
        return_value=expected_ticket_number
    )

@pytest.fixture
def expected_booking_reference() -> BookingReference:
    return "ABC123"

@pytest.fixture
def expected_ticket_number() -> TicketNumber:
    return "1234567890123"

@pytest.fixture
def expected_booking_id() -> BookingId:
    return UUID("12345678-1234-5678-1234-567812345678")