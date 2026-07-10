from fastapi import APIRouter, Depends

from src.api.schemas import BookingRequest, BookingResponse
from src.common import DBManager
from src.core.validators import FlightValidator, PassengerValidator
from src.core.use_cases import CreateBooking, PassengerProcessor, CreateBookingValidator
from src.core.units_of_work import CreateBookingUoW

router = APIRouter(prefix="/api/flights", tags=["Flights"])

def get_booking_creator() -> CreateBooking:
    db_manager = DBManager()
    passenger_processor = PassengerProcessor()
    create_booking_validator = CreateBookingValidator(FlightValidator(), PassengerValidator())

    return CreateBooking(CreateBookingUoW(db_manager), passenger_processor, create_booking_validator)

@router.post("/", response_model=BookingResponse)
def create_booking(booking_request: BookingRequest, booking_creator: CreateBooking = Depends(get_booking_creator)):
    booking_response: BookingResponse = booking_creator.execute(booking_request)

    return booking_response