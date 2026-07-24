from src.api.schemas import BookingRequest, BookingResponse, PassengerRequest
from src.common.exceptions import (BlacklistedPassenger, FullFlight,
                                   InexistentFlight, InvalidData,
                                   MultipleExceptionsError, NotScheduledFlight,
                                   NotSeatsEnough)
from src.common.types import (BasePriceUsd, DocumentIdentityKey, FlightId,
                              PassengerId)
from src.core.units_of_work import RegisterBookingUoW
from src.core.validators import (BaseValidator, FlightValidator,
                                 PassengerValidator)
from src.entities import Booking, Document, Flight, Passenger, Ticket


class PassengerProcessor:

    def get_or_create_passengers(
        self,
        passengers_requested: list[PassengerRequest],
        documents_retrieved: list[Document],
    ) -> tuple[list[Passenger], list[Document], list[PassengerId]]:
        passengers_not_in_db: list[Passenger] = []
        documents_not_in_db: list[Document] = []
        all_passengers_id: list[PassengerId] = []

        documents_retrieved_identity_keys: dict[DocumentIdentityKey, PassengerId] = {
            document.identity_key: document.passenger_id
            for document in documents_retrieved
        }
        for passenger in passengers_requested:
            if passenger.identity_key not in documents_retrieved_identity_keys:
                passenger_created = Passenger.new_passenger(
                    full_name=passenger.full_name,
                    birth_date=passenger.birth_date,
                    email=passenger.email,
                    phone_number=passenger.phone_number,
                )

                document_created = Document.new_document(
                    document_number=passenger.document_number,
                    valid_from=passenger.valid_from,
                    valid_until=passenger.valid_until,
                    issue_country=passenger.issue_country,
                    passenger_id=passenger_created.id,
                    document_type_id=passenger.document_type_id,
                )

                passengers_not_in_db.append(passenger_created)
                documents_not_in_db.append(document_created)
                all_passengers_id.append(passenger_created.id)

            else:
                all_passengers_id.append(
                    documents_retrieved_identity_keys[passenger.identity_key]
                )

        return passengers_not_in_db, documents_not_in_db, all_passengers_id


class RegisterBookingValidator:

    def __init__(
        self,
        base_validator: BaseValidator,
        flight_validator: FlightValidator,
        passenger_validator: PassengerValidator,
    ) -> None:
        self.base_validator = base_validator
        self.flight_validator = flight_validator
        self.passenger_validator = passenger_validator

    def validate_data_logic(
        self, flights_requested_id: list[FlightId], flights_retrieved_id: list[FlightId]
    ) -> None:
        exceptions: list[InvalidData] = []

        flights_missing_ids: set[FlightId] = self.base_validator.check_existence(
            flights_requested_id, flights_retrieved_id
        )

        for flight_id in flights_missing_ids:
            exceptions.append(InexistentFlight(flight_id))

        if exceptions:
            raise MultipleExceptionsError(exceptions)

    def validate_business_logic(
        self,
        all_passengers: list[Passenger],
        flights_retrieved: list[Flight],
        seats_available_per_flight: dict[FlightId, int],
    ) -> None:
        exceptions: list[InvalidData] = []

        full_flights_ids, not_seats_enough_flights_ids = (
            self.flight_validator.check_seats_available(
                seats_available_per_flight, len(all_passengers)
            )
        )
        not_scheduled_flights_ids: list[FlightId] = (
            self.flight_validator.check_statuses(flights_retrieved)
        )
        passengers_blacklisted_ids: list[FlightId] = (
            self.passenger_validator.is_blacklisted(all_passengers)
        )

        for flight_id in full_flights_ids:
            exceptions.append(FullFlight(flight_id))

        for flight_id in not_seats_enough_flights_ids:
            exceptions.append(NotSeatsEnough(flight_id))

        for flight_id in not_scheduled_flights_ids:
            exceptions.append(NotScheduledFlight(flight_id))

        for passenger_id in passengers_blacklisted_ids:
            exceptions.append(BlacklistedPassenger(passenger_id))

        if exceptions:
            raise MultipleExceptionsError(exceptions)


class RegisterBooking:

    def __init__(
        self,
        uow: RegisterBookingUoW,
        passenger_processor: PassengerProcessor,
        register_booking_validator: RegisterBookingValidator,
    ) -> None:

        self.uow = uow
        self.passenger_processor = passenger_processor
        self.register_booking_validator = register_booking_validator

    def execute(self, booking_request: BookingRequest) -> BookingResponse:
        with self.uow as uow:
            flight_requested_ids: list[FlightId] = booking_request.flights_id
            flights_retrieved: list[Flight] = uow.flight_repository.retrieve_by_ids(
                booking_request.flights_id
            )
            flight_retrieved_ids: list[FlightId] = [
                flight.id for flight in flights_retrieved
            ]

            self.register_booking_validator.validate_data_logic(
                flight_requested_ids, flight_retrieved_ids
            )

            seats_available_per_flight: dict[FlightId, int] = (
                uow.flight_repository.retrieve_seats_available_per_flight(
                    flight_retrieved_ids
                )
            )

            passengers_requested: list[PassengerRequest] = booking_request.passengers
            document_requested_identity_keys: list[DocumentIdentityKey] = [
                passenger.identity_key for passenger in passengers_requested
            ]

            documents_retrieved: list[Document] = (
                uow.document_repository.retrieve_by_identity_keys(
                    document_requested_identity_keys
                )
            )

            passengers_not_in_db, documents_not_in_db, all_passengers_ids = (
                self.passenger_processor.get_or_create_passengers(
                    passengers_requested, documents_retrieved
                )
            )

            if passengers_not_in_db:
                uow.passenger_repository.insert(passengers_not_in_db)

            if documents_not_in_db:
                uow.document_repository.insert(documents_not_in_db)

            all_passengers: list[Passenger] = uow.passenger_repository.retrieve_by_ids(
                all_passengers_ids
            )

            self.register_booking_validator.validate_business_logic(
                all_passengers, flights_retrieved, seats_available_per_flight
            )

            flight_retrieved_base_prices: list[BasePriceUsd] = [
                flight.base_price_usd for flight in flights_retrieved
            ]

            booking_created = Booking.new_booking(
                flight_retrieved_base_prices, len(all_passengers_ids)
            )
            uow.booking_repository.insert([booking_created])

            tickets_created: list[Ticket] = booking_created.generate_tickets(
                all_passengers_ids, flights_retrieved, booking_created.id
            )

            uow.ticket_repository.insert(tickets_created)

            return BookingResponse(
                booking_reference=booking_created.booking_reference,
                tickets=[ticket.ticket_number for ticket in tickets_created],
                paid_amount_usd=booking_created.paid_amount_usd,
            )
