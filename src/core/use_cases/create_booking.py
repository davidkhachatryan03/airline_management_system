from src.core.units_of_work import CreateBookingUoW
from src.core.managers import PassengerManager
from src.entities import Document, Passenger
from src.api.schemas import BookingRequest, PassengerRequest
from src.common.exceptions import InsertionMissmatchError
from uuid import UUID
import uuid6

class CreateBooking:

    def __init__(self,
                uow: CreateBookingUoW,
                passenger_manager: PassengerManager,
                flight_validator) -> None:
        
        self.uow = uow
        self.passenger_manager = passenger_manager
        self.flight_validator = flight_validator
    
    def process_booking(self, booking_request: BookingRequest) -> None:
        with self.uow as uow:
            self.flight_validator.check_flights_availability(booking_request.flights_id)q