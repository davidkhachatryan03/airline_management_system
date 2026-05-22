from src.core.repositories import BookingRepository
from src.entities import Booking
from src.api.schemas import BookingResponse, BookingRequest

class BookingValidator:

    def __init__(self, booking_repository: BookingRepository) -> None:
        self.booking_repository = booking_repository