from src.core.units_of_work import CreateBookingUoW
from src.core.validators import FlightValidator, PassengerValidator
from src.entities import Flight, Document, Passenger, Booking, Ticket
from src.api.schemas import BookingRequest, BookingResponse, PassengerRequest
from uuid import UUID
from decimal import Decimal

class PassengerProcessor:
    
    def process(self, passengers_requested: list[PassengerRequest], documents_retrieved: list[Document]) -> tuple[list[Passenger], list[Document], list[UUID]]:
        passengers_not_in_db: list[Passenger] = []
        documents_not_in_db: list[Document] = []
        all_passengers_id: list[UUID] = []
        
        dict_documents_retrieved: dict = {(document.document_number, document.valid_from, document.valid_until, document.issue_country, document.document_type_id): document.passenger_id for document in documents_retrieved}
        for passenger in passengers_requested:
            if (passenger.document_number, passenger.valid_from, passenger.valid_until, passenger.issue_country, passenger.document_type_id) not in dict_documents_retrieved:

                passenger_not_in_db = Passenger.new_passenger(
                    full_name=passenger.full_name,
                    birth_date=passenger.birth_date,
                    email=passenger.email,
                    phone_number=passenger.phone_number
                )

                document_not_in_db = Document.new_document(
                    document_number=passenger.document_number,
                    valid_from=passenger.valid_from,
                    valid_until=passenger.valid_until,
                    issue_country=passenger.issue_country,
                    passenger_id=passenger_not_in_db.id,
                    document_type_id=passenger.document_type_id
                )

                passengers_not_in_db.append(passenger_not_in_db)
                all_passengers_id.append(passenger_not_in_db.id)
                documents_not_in_db.append(document_not_in_db)
            
            else:

                all_passengers_id.append(dict_documents_retrieved[(passenger.document_number, passenger.valid_from, passenger.valid_until, passenger.issue_country, passenger.document_type_id)])

        return passengers_not_in_db, documents_not_in_db, all_passengers_id
    
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

            seats_available_per_flight: list[tuple[UUID, int]] = uow.flight_repository.retrieve_seats_available_per_flight(flights_retrieved)
            self.flight_validator.check_seats_available_per_flight(seats_available_per_flight, len(booking_request.passengers))

            passengers_requested: list[PassengerRequest] = booking_request.passengers
            documents_requested: list[tuple] = [(passenger.document_number, passenger.valid_from, passenger.valid_until, passenger.issue_country, passenger.document_type_id) for passenger in passengers_requested]
            documents_retrieved: list[Document] = uow.document_repository.retrieve_documents(documents_requested)

            passengers_not_in_db, documents_not_in_db, all_passengers_id = self.passenger_processor.process(passengers_requested, documents_retrieved)

            if passengers_not_in_db:
                uow.passenger_repository.insert_passengers(passengers_not_in_db)

            if documents_not_in_db:
                uow.document_repository.insert_documents(documents_not_in_db)

            all_passengers: list[Passenger] = uow.passenger_repository.retrieve_passengers(all_passengers_id)
            self.passenger_validator.check_blacklisted(all_passengers)

            paid_amount_usd: Decimal = self._calculate_paid_amount_usd(flights_retrieved, len(all_passengers_id))

            booking_created = Booking.new_booking(paid_amount_usd)
            self.uow.booking_repository.insert_booking(booking_created)

            tickets_created: list[Ticket] = self._generate_tickets(all_passengers_id, flights_retrieved, booking_created.id)

            self.uow.ticket_repository.insert_tickets(tickets_created)

            return BookingResponse(
                booking_reference=booking_created.booking_reference,
                tickets=[ticket.ticket_number for ticket in tickets_created],
                paid_amount_usd=paid_amount_usd
            )

    def _calculate_paid_amount_usd(self, flights: list[Flight], number_of_passengers: int) -> Decimal:
        paid_amount_usd: Decimal = sum((flight.base_price_usd for flight in flights), Decimal("0")) * number_of_passengers

        return paid_amount_usd
    
    def _generate_tickets(self, passengers_id: list[UUID], flights: list[Flight], booking_id: UUID) -> list[Ticket]:
        tickets_created: list[Ticket] = []
        
        for passenger_id in passengers_id:
            for flight in flights: 
                ticket_created = Ticket.new_ticket(
                    paid_amount_usd=flight.base_price_usd,
                    booking_id=booking_id,
                    flight_id=flight.id,
                    passenger_id=passenger_id
                )
                
                tickets_created.append(ticket_created)
        
        return tickets_created