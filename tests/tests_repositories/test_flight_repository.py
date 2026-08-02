from factory.declarations import Iterator

from src.common.types import FlightId, PassengerId
from src.core.repositories import (
    AirplaneRepository,
    BookingRepository,
    FlightRepository,
    PassengerRepository,
    TicketRepository,
)
from src.entities import Airplane, Booking, Flight, Passenger, Ticket
from tests.factories import (
    AirplaneFactory,
    BookingFactory,
    FlightFactory,
    PassengerFactory,
    TicketFactory,
)


def test_retrieve_seats_available_per_flight(
    airplane_repository: AirplaneRepository,
    booking_repository: BookingRepository,
    flight_repository: FlightRepository,
    passenger_repository: PassengerRepository,
    ticket_repository: TicketRepository,
) -> None:
    airplane_repository.delete()

    airplane_1: Airplane = AirplaneFactory(capacity=100)
    airplane_2: Airplane = AirplaneFactory(capacity=150)
    airplane_repository.insert([airplane_1, airplane_2])

    booking: Booking = BookingFactory()
    booking_repository.insert([booking])

    flight_1: Flight = FlightFactory(airplane_id=airplane_1.id)
    flight_2: Flight = FlightFactory(airplane_id=airplane_2.id)
    flight_repository.insert([flight_1, flight_2])

    passengers: list[Passenger] = PassengerFactory.build_batch(30)
    passenger_ids: list[PassengerId] = [passenger.id for passenger in passengers]
    passenger_repository.insert(passengers)

    tickets_flight_1: list[Ticket] = TicketFactory.build_batch(
        30,
        flight_id=flight_1.id,
        passenger_id=Iterator(passenger_ids),
        booking_id=booking.id,
    )
    ticket_repository.insert(tickets_flight_1)

    seats_available_per_flight_expected = {flight_1.id: 70, flight_2.id: 150}

    flight_ids: list[FlightId] = [flight_1.id, flight_2.id]

    seats_available_per_flight_retrieved = (
        flight_repository.retrieve_seats_available_per_flight(flight_ids)
    )

    assert seats_available_per_flight_retrieved == seats_available_per_flight_expected
