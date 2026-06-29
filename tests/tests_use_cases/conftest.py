from datetime import datetime, date
from decimal import Decimal
import pytest
from uuid import UUID

from src.api.schemas import BookingRequest, PassengerRequest
from src.entities import Passenger, Flight

@pytest.fixture
def booking_request() -> BookingRequest:
    return BookingRequest(
        flights_id=[UUID("019eb14c-ed68-7e52-a495-8a80b519a12f")], 
        passengers=[
            PassengerRequest(
            full_name="David Khachatryan",
            birth_date=date(2000,1,1),
            national_identity_number="40123789",
            email="email@example.com",
            phone_number="1234567890",
            valid_from=date(2023,1,1),
            valid_until=date(2033,1,1),
            issue_country="ARG"
        ),
            PassengerRequest(
            full_name="John Doe",
            birth_date=date(1980,1,1),
            national_identity_number="13555432",
            email="jhon@example.com",
            phone_number="9876543210",
            valid_from=date(2025,1,1),
            valid_until=date(2035,1,1),
            issue_country="USA"
        )
        ]
    )

@pytest.fixture
def passengers_generated(booking_request: BookingRequest) -> list[Passenger]:
    passengers: list[Passenger] = []

    passengers_requested: list[PassengerRequest] = booking_request.passengers

    for passenger in passengers_requested:
        
        passenger_created = Passenger.new_passenger(
            full_name=passenger.full_name,
            birth_date=passenger.birth_date,
            national_identity_number=passenger.national_identity_number,
            issue_country=passenger.issue_country,
            email=passenger.email,
            phone_number=passenger.phone_number
            )

        passengers.append(passenger_created)
    
    return passengers

@pytest.fixture
def flights_generated(booking_request: BookingRequest) -> list[Flight]:
    flights: list[Flight] = []
    flights_id: list[UUID] = booking_request.flights_id

    for id in flights_id:
        flight = Flight.new_flight(
            scheduled_departure_datetime=datetime(2025,1,1),
            scheduled_arrival_datetime=datetime(2025,1,2),
            operating_cost_usd=Decimal("10000.78"),
            route_id=1,
            airplane_id=1
        )

        flight.id = id

        flights.append(flight)
    
    return flights

@pytest.fixture
def fixed_booking_identifiers(mocker):
    mocker.patch(
        "src.entities.Booking._generate_reference",
        return_value="ABC123"
    )

    mocker.patch(
        "src.entities.Ticket._generate_ticket_number",
        return_value="1234567890123"
    )

@pytest.fixture
def expected_booking_reference() -> str:
    return "ABC123"

@pytest.fixture
def expected_ticket_number() -> str:
    return "1234567890123"