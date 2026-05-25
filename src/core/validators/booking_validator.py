from src.core.repositories import BookingRepository
from src.api.schemas import BookingRequest
from uuid import UUID
from decimal import Decimal
from src.entities import Passenger, Flight
from src.common.exceptions import InvalidPassengerBlacklisted, InvalidPassengerId ,InvalidFlightId, InvalidPaidAmountUsd

class BookingValidator:

    def __init__(self, booking_repository: BookingRepository) -> None:
        self.booking_repository = booking_repository

    def validate_booking_request(self, booking_request: BookingRequest) -> bool:
        passengers_id: list[UUID] = booking_request.passengers_id
        flights_id: list[UUID] = booking_request.flights_id
        paid_amount_usd: Decimal = booking_request.paid_amount_usd

        for passenger_id in passengers_id:
            self.check_passenger(passenger_id)
            
        for flight_id in flights_id:
            if not self.check_flight(flight_id):
                raise InvalidFlightId("The flight does not exist.")
        
        for flight_id in flights_id:
            if not self.check_paid_amount_usd(paid_amount_usd, flight_id, len(passengers_id)):
                raise InvalidPaidAmountUsd("The paid amount is incorrect.")
        
        return True

    def check_passenger(self, passenger_id: UUID) -> bool:
        passenger: Passenger = self.booking_repository.retrieve_passenger(passenger_id)

        if passenger.id != passenger_id:
            raise InvalidPassengerId("The passenger does not exist.")
        
        if passenger.is_blacklisted:
            raise InvalidPassengerBlacklisted("The passenger is blacklisted.")

        return (passenger.id == passenger_id and not passenger.is_blacklisted)
    
    def check_flight(self, flight_id: UUID) -> bool:
        flight: Flight = self.booking_repository.retrieve_flight(flight_id)

        return flight.id == flight_id
    
    def check_paid_amount_usd(self, paid_amount_usd: Decimal, flight_id: UUID, passengers_number: int) -> bool:
        calculated_paid_amount_usd: Decimal = self.booking_repository.retrieve_paid_amount_usd(flight_id, passengers_number)

        return calculated_paid_amount_usd == paid_amount_usd