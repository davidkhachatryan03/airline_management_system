from src.core.repositories import BookingRepository
from src.core.validators import BookingValidator


class BookingManager:

    def __init__(self, booking_validator: BookingValidator) -> None:
        self.booking_validator = booking_validator