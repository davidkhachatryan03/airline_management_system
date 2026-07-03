from uuid import UUID

from src.api.schemas import BookingRequest, BookingResponse, PassengerRequest
from src.entities import Booking, Flight, Passenger, Ticket
from src.core.units_of_work import CreateBookingUoW
from src.core.validators import FlightValidator, PassengerValidator

class PassengerProcessor:
    
    def get_or_create_passengers(self, passengers_requested: list[PassengerRequest], passengers_retrieved: list[Passenger]) -> tuple[list[Passenger], list[UUID]]:
        passengers_not_in_db: list[Passenger] = []
        all_passengers_id: list[UUID] = []
        
        dict_passengers_retrieved_identity_keys: dict[tuple, UUID] = {passenger.identity_key: passenger.id for passenger in passengers_retrieved}
        for passenger in passengers_requested:
            if passenger.identity_key not in dict_passengers_retrieved_identity_keys:

                passenger_not_in_db = Passenger.new_passenger(
                    full_name=passenger.full_name,
                    national_identity_number=passenger.national_identity_number,
                    issue_country=passenger.issue_country,
                    birth_date=passenger.birth_date,
                    email=passenger.email,
                    phone_number=passenger.phone_number
                )

                passengers_not_in_db.append(passenger_not_in_db)
                all_passengers_id.append(passenger_not_in_db.id)
            
            else:

                all_passengers_id.append(dict_passengers_retrieved_identity_keys[passenger.identity_key])

        return passengers_not_in_db, all_passengers_id
    
class CreateBooking:

    def __init__(self,
                uow: CreateBookingUoW,
                passenger_processor: PassengerProcessor,
                flight_validator: FlightValidator,
                passenger_validator: PassengerValidator) -> None:
        
        self.uow = uow
        self.passenger_processor = passenger_processor
        self.flight_validator = flight_validator
        self.passenger_validator = passenger_validator
    
    def execute(self, booking_request: BookingRequest) -> BookingResponse:
        with self.uow as uow:
            flights_retrieved: list[Flight] = uow.flight_repository.retrieve_flights_by_id(booking_request.flights_id)
            self.flight_validator.check_flights_existence(booking_request.flights_id, flights_retrieved)

            seats_available_per_flight: dict[UUID, int] = uow.flight_repository.retrieve_seats_available_per_flight(flights_retrieved)
            self.flight_validator.check_seats_available_per_flight(seats_available_per_flight, len(booking_request.passengers))

            self.flight_validator.check_flights_statuses(flights_retrieved)

            passengers_requested: list[PassengerRequest] = booking_request.passengers
            passengers_requested_documents: list[tuple] = [passenger.identity_key for passenger in passengers_requested]

            passengers_retrieved: list[Passenger] = uow.passenger_repository.retrieve_passengers_by_document(passengers_requested_documents)

            passengers_not_in_db, all_passengers_id = self.passenger_processor.get_or_create_passengers(passengers_requested, passengers_retrieved)

            if passengers_not_in_db:
                uow.passenger_repository.insert_passengers(passengers_not_in_db)

            all_passengers: list[Passenger] = uow.passenger_repository.retrieve_passengers_by_id(all_passengers_id)
            self.passenger_validator.check_blacklisted(all_passengers)

            booking_created = Booking.new_booking(flights_retrieved, len(all_passengers))
            uow.booking_repository.insert_booking(booking_created)

            tickets_created: list[Ticket] = booking_created.generate_tickets(all_passengers_id, flights_retrieved, booking_created.id)

            uow.ticket_repository.insert_tickets(tickets_created)

            return BookingResponse(
                booking_reference=booking_created.booking_reference,
                tickets=[ticket.ticket_number for ticket in tickets_created],
                paid_amount_usd=booking_created.paid_amount_usd
            )