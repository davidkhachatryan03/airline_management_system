from fastapi import APIRouter, Depends

from src.api.schemas import BookingRequest, BookingResponse
from src.common import DBManager
from src.core.validators import BaseValidator, FlightValidator, PassengerValidator
from src.core.use_cases import PassengerProcessor, RegisterBooking, RegisterBookingValidator
from src.core.units_of_work import RegisterBookingUoW

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

def create_register_booking() -> RegisterBooking:
    db_manager = DBManager()
    base_validator = BaseValidator()
    flight_validator = FlightValidator()
    passenger_validator = PassengerValidator()

    return RegisterBooking(RegisterBookingUoW(db_manager), PassengerProcessor(), RegisterBookingValidator(base_validator, flight_validator, passenger_validator))

@router.post("/", response_model=BookingResponse)
def create_booking(booking_request: BookingRequest, register_booking: RegisterBooking = Depends(create_register_booking)):
    booking_response: BookingResponse = register_booking.execute(booking_request)

    return booking_response