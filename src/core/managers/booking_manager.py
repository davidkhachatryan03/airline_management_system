from src.core.repositories import BookingRepository
from src.core.validators import BookingValidator
from src.entities import BookingCreated, BookingRetrieved

class BookingManager:

    def __init__(self, booking_repository: BookingRepository, booking_validator: BookingValidator) -> None:
        self.booking_repository = booking_repository
        self.booking_validator = booking_validator

    def create_booking(self, booking_created: BookingCreated) -> int:
        inserted_booking_id: int = self.booking_repository.insert_booking(booking_created)
        
        return inserted_booking_id