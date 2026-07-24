from src.entities import Booking


class FakeBookingRepository:

    def __init__(self) -> None:
        self.bookings: list[Booking] = []

    def insert(self, bookings: list[Booking]) -> None:
        for booking in bookings:
            self.bookings.append(booking)
