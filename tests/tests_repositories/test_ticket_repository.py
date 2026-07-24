from src.core.repositories import (BookingRepository, FlightRepository,
                                PassengerRepository, TicketRepository)
from src.entities import Booking, Flight, Passenger, Ticket


def test_insert_ticket(
    ticket_repository: TicketRepository,
    booking_repository: BookingRepository,
    flight_repository: FlightRepository,
    passenger_repository: PassengerRepository,
    ticket: Ticket,
    booking: Booking,
    flight: Flight,
    passenger: Passenger,
) -> None:
    booking_repository.insert([booking])
    flight_repository.insert([flight])
    passenger_repository.insert([passenger])
    ticket_repository.insert([ticket])

    last_inserted_ticket: Ticket = ticket_repository.retrieve(limit=1)[0]

    assert last_inserted_ticket == ticket


def test_retrieve_all_tickets(
    ticket_repository: TicketRepository,
    booking_repository: BookingRepository,
    flight_repository: FlightRepository,
    passenger_repository: PassengerRepository,
    tickets: list[Ticket],
    booking: Booking,
    flight: Flight,
    passengers: list[Passenger],
) -> None:
    booking_repository.insert([booking])
    flight_repository.insert([flight])
    passenger_repository.insert(passengers)
    ticket_repository.insert(tickets)

    all_inserted_tickets: list[Ticket] = ticket_repository.retrieve(limit=3)

    assert len(all_inserted_tickets) == len(tickets)
