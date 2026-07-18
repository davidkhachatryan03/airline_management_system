from src.core.repositories import BookingRepository
from src.entities import Booking


def test_insert_booking(
    booking_repository: BookingRepository, booking: Booking
) -> None:
    booking_repository.insert_booking(booking)

    last_inserted_booking: Booking = booking_repository.retrieve_bookings(limit=1)[0]

    assert last_inserted_booking.id == booking.id
    assert last_inserted_booking.booking_reference == booking.booking_reference
    assert type(last_inserted_booking.booking_datetime) == type(
        booking.booking_datetime
    )
    assert last_inserted_booking.paid_amount_usd == booking.paid_amount_usd
    assert last_inserted_booking.current_status_id == booking.current_status_id


def test_retrieve_all_bookings(
    booking_repository: BookingRepository, bookings: list[Booking]
) -> None:
    for booking in bookings:
        booking_repository.insert_booking(booking)

    all_inserted_bookings: list[Booking] = booking_repository.retrieve_bookings(limit=3)

    assert len(all_inserted_bookings) == len(bookings)
