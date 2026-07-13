from src.api.schemas import BookingRequest, BookingResponse, PassengerRequest
from src.entities import Booking, Flight, Passenger, Ticket
from src.common.exceptions import InexistentFlight, FullFlight, NotScheduledFlight, BlacklistedPassenger, MultipleExceptionsError
from src.common.types import PassengerId, PassengerIdentityKey, FlightId, IsBlacklisted, CurrentStatusId, BasePriceUsd
from src.core.units_of_work import CreateBookingUoW
from src.core.validators import BaseValidator, FlightValidator, PassengerValidator

class PassengerProcessor:
    
    def get_or_create_passengers(self, passengers_requested: list[PassengerRequest], passengers_retrieved: list[Passenger]) -> tuple[list[Passenger], list[PassengerId]]:
        passengers_not_in_db: list[Passenger] = []
        all_passengers_id: list[PassengerId] = []
        
        dict_passengers_retrieved_identity_keys: dict[PassengerIdentityKey, PassengerId] = {passenger.identity_key: passenger.id for passenger in passengers_retrieved}
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
    
class CreateBookingValidator:
    
    def __init__(self, base_validator: BaseValidator, flight_validator: FlightValidator, passenger_validator: PassengerValidator) -> None:
        self.base_validator = base_validator
        self.flight_validator = flight_validator
        self.passenger_validator = passenger_validator

    def validate_data_logic(self, flights_requested_id: list[FlightId], flights_retrieved_id: list[FlightId]) -> None:
        if not self.base_validator.check_existence(flights_requested_id, flights_retrieved_id):
            raise InexistentFlight

    def validate_business_logic(self, passengers_statuses: list[IsBlacklisted], flights_retrieved_statuses: list[CurrentStatusId], seats_available_per_flight: dict[FlightId, int]) -> None:
        exceptions: list[Exception] = []

        if not self.flight_validator.check_seats_available(seats_available_per_flight, len(passengers_statuses)):
            exceptions.append(FullFlight())
        
        if not self.flight_validator.check_statuses(flights_retrieved_statuses):
            exceptions.append(NotScheduledFlight())
        
        if  self.passenger_validator.is_blacklisted(passengers_statuses):
            exceptions.append(BlacklistedPassenger())
        
        if exceptions:
            raise MultipleExceptionsError(exceptions)
        
class CreateBooking:

    def __init__(self,
                uow: CreateBookingUoW,
                passenger_processor: PassengerProcessor,
                create_booking_validator: CreateBookingValidator) -> None:
        
        self.uow = uow
        self.passenger_processor = passenger_processor
        self.create_booking_validator = create_booking_validator
    
    def execute(self, booking_request: BookingRequest) -> BookingResponse:
        with self.uow as uow:
            flights_requested_id: list[FlightId] = booking_request.flights_id
            flights_retrieved: list[Flight] = uow.flight_repository.retrieve_flights_by_id(booking_request.flights_id)
            flights_retrieved_id: list[FlightId] = [flight.id for flight in flights_retrieved]

            self.create_booking_validator.validate_data_logic(flights_requested_id, flights_retrieved_id)

            seats_available_per_flight: dict[FlightId, int] = uow.flight_repository.retrieve_seats_available_per_flight(flights_retrieved_id)

            passengers_requested: list[PassengerRequest] = booking_request.passengers
            passengers_requested_documents: list[PassengerIdentityKey] = [passenger.identity_key for passenger in passengers_requested]

            passengers_retrieved: list[Passenger] = uow.passenger_repository.retrieve_passengers_by_document(passengers_requested_documents)

            passengers_not_in_db, all_passengers_id = self.passenger_processor.get_or_create_passengers(passengers_requested, passengers_retrieved)

            if passengers_not_in_db:
                uow.passenger_repository.insert_passengers(passengers_not_in_db)

            all_passengers: list[Passenger] = uow.passenger_repository.retrieve_passengers_by_id(all_passengers_id)
            all_passengers_statuses: list[IsBlacklisted] = [passenger.is_blacklisted for passenger in all_passengers]

            flights_retrieved_statuses: list[CurrentStatusId] = [flight.current_status_id for flight in flights_retrieved]

            self.create_booking_validator.validate_business_logic(all_passengers_statuses, flights_retrieved_statuses, seats_available_per_flight)

            flights_retrieved_base_prices: list[BasePriceUsd] = [flight.base_price_usd for flight in flights_retrieved]

            booking_created = Booking.new_booking(flights_retrieved_base_prices, len(all_passengers_id))
            uow.booking_repository.insert_booking(booking_created)

            tickets_created: list[Ticket] = booking_created.generate_tickets(all_passengers_id, flights_retrieved, booking_created.id)

            uow.ticket_repository.insert_tickets(tickets_created)

            return BookingResponse(
                booking_reference=booking_created.booking_reference,
                tickets=[ticket.ticket_number for ticket in tickets_created],
                paid_amount_usd=booking_created.paid_amount_usd
            )