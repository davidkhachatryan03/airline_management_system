from src.entities import Booking


class FakeBookingRepository:

    def __init__(self) -> None:
        self.bookings: list[Booking] = []

    def insert_booking(self, booking: Booking) -> None:
        self.bookings.append(booking)
