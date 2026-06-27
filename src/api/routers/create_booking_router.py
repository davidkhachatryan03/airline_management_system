from fastapi import APIRouter, Depends
from src.api.schemas import BookingRequest, BookingResponse
from src.core.validators import FlightValidator, PassengerValidator
from src.common import DBManager
from src.core.use_cases import CreateBooking, PassengerProcessor
from src.core.units_of_work import CreateBookingUoW

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

def get_booking_creator() -> CreateBooking:
    db_manager = DBManager()
    passenger_processor = PassengerProcessor()
    flight_validator = FlightValidator()
    passenger_validator = PassengerValidator()

    return CreateBooking(CreateBookingUoW(db_manager), passenger_processor, flight_validator, passenger_validator)

@router.post("/", response_model=BookingResponse)
def create_booking(booking_request: BookingRequest, booking_creator = Depends(get_booking_creator)):
    booking_response: BookingResponse = booking_creator.execute(booking_request)

    return booking_response