from src.core.repositories import BookingRepository
from src.api.schemas import BookingRequest
from uuid import UUID
from decimal import Decimal

class BookingValidator:

    def __init__(self, booking_repository: BookingRepository) -> None:
        self.booking_repository = booking_repository

    def validate_booking_request(self, booking_request: BookingRequest) -> bool:
        passengers_id: list[UUID] = booking_request.passengers_id
        flights_id: list[UUID] = booking_request.flights_id
        paid_amount_usd: Decimal = booking_request.paid_amount_usd

        for passenger_id in passengers_id:
            if not self.check_passenger_id(passenger_id):
                return False
            
        for flight_id in flights_id:
            if not self.check_flight_id(flight_id):
                return False
        
        for flight_id in flights_id:
            if not self.check_paid_amount_usd(paid_amount_usd, flight_id):
                return False
        
        return True

    def check_passenger_id(self, passenger_id: UUID) -> bool:
        result: UUID = self.booking_repository.retrieve_passenger_id(passenger_id)

        return result == passenger_id
    
    def check_flight_id(self, flight_id: UUID) -> bool:
        result: UUID = self.booking_repository.retrieve_flight_id(flight_id)

        return result == flight_id
    
    def check_paid_amount_usd(self, paid_amount_usd: Decimal, flight_id: UUID) -> bool:
        result: Decimal = self.booking_repository.retrieve_paid_amount_usd(flight_id)

        return result == paid_amount_usd