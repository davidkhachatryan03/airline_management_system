from fastapi import APIRouter, Depends

from src.api.schemas import FlightRequest, FlightResponse
from src.common import DBManager
from src.core.units_of_work import RegisterFlightUoW
from src.core.use_cases import RegisterFlight, RegisterFlightValidator
from src.core.validators import BaseValidator, FlightValidator

router = APIRouter(prefix="/api/flights", tags=["Bookings"])


def create_register_flight() -> RegisterFlight:
    db_manager = DBManager()
    base_validator = BaseValidator()
    flight_validator = FlightValidator()

    return RegisterFlight(
        RegisterFlightUoW(db_manager),
        RegisterFlightValidator(base_validator, flight_validator),
    )


@router.post("/", response_model=FlightResponse)
def register_flight(
    flight_request: FlightRequest,
    register_flight: RegisterFlight = Depends(create_register_flight),
):
    flight_response: FlightResponse = register_flight.execute(flight_request)

    return flight_response
