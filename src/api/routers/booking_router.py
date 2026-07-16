from fastapi import APIRouter, Depends

from src.api.schemas import BookingRequest, BookingResponse
from src.common import DBManager
from src.core.validators import BaseValidator, FlightValidator, PassengerValidator
from src.core.use_cases import PassengerProcessor, RegisterBooking, RegisterBookingValidator
from src.core.units_of_work import CreateBookingUoW

router = APIRouter(prefix="/api/flights", tags=["Flights"])

def get_booking_creator() -> RegisterBooking:
    db_manager = DBManager()
    base_validator = BaseValidator()
    flight_validator = FlightValidator()
    passenger_validator = PassengerValidator()

    return RegisterBooking(CreateBookingUoW(db_manager), PassengerProcessor(), RegisterBookingValidator(base_validator, flight_validator, passenger_validator))

@router.post("/", response_model=BookingResponse)
def create_booking(booking_request: BookingRequest, booking_creator: RegisterBooking = Depends(get_booking_creator)):
    booking_response: BookingResponse = booking_creator.execute(booking_request)

    return booking_response