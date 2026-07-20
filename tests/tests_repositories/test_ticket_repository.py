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
    booking_repository.insert_booking(booking)
    flight_repository.insert_flights([flight])
    passenger_repository.insert_passengers([passenger])
    ticket_repository.insert_tickets([ticket])

    last_inserted_ticket: Ticket = ticket_repository.retrieve_tickets(limit=1)[0]

    assert last_inserted_ticket.id == ticket.id
    assert last_inserted_ticket.ticket_number == ticket.ticket_number
    assert last_inserted_ticket.paid_amount_usd == ticket.paid_amount_usd
    assert last_inserted_ticket.current_status_id == ticket.current_status_id
    assert last_inserted_ticket.booking_id == ticket.booking_id
    assert last_inserted_ticket.flight_id == ticket.flight_id
    assert last_inserted_ticket.passenger_id == ticket.passenger_id


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
    booking_repository.insert_booking(booking)
    flight_repository.insert_flights([flight])
    passenger_repository.insert_passengers(passengers)
    ticket_repository.insert_tickets(tickets)

    all_inserted_tickets: list[Ticket] = ticket_repository.retrieve_tickets(limit=3)

    assert len(all_inserted_tickets) == len(tickets)
