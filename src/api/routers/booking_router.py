from fastapi import APIRouter, HTTPException
from src.api.schemas.booking_schema import BookingRequest, BookingResponse
from src.core.managers.booking_manager import BookingManager
from src.core.validators.booking_validator import BookingValidator
from src.core.repositories.booking_repository import BookingRepository
from src.common import DBManager

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingResponse)
def create_booking(booking_request: BookingRequest):

    db_manager = DBManager()

    booking_repository = BookingRepository(db_manager)
    booking_validator = BookingValidator(booking_repository)
    booking_manager = BookingManager(booking_repository, booking_validator)

    try:
        booking_response = booking_manager.process_booking(booking_request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error.")

    return booking_response