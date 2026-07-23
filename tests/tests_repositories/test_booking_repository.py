from src.core.repositories import BookingRepository
from src.entities import Booking

def test_insert_booking(
    booking_repository: BookingRepository, booking: Booking
) -> None:
    booking_repository.insert_booking(booking)

    last_inserted_booking: Booking = booking_repository.retrieve_bookings(limit=1)[0]

    assert last_inserted_booking == booking


def test_retrieve_all_bookings(
    booking_repository: BookingRepository, bookings: list[Booking]
) -> None:
    for booking in bookings:
        booking_repository.insert_booking(booking)

    all_inserted_bookings: list[Booking] = booking_repository.retrieve_bookings(limit=3)

    assert len(all_inserted_bookings) == len(bookings)
