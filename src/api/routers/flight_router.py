from fastapi import APIRouter, Depends

from src.api.schemas import FlightRequest, FlightResponse
from src.common import DBManager
from src.core.validators import AirplaneValidator, FlightValidator, RouteValidator
from src.core.use_cases import RegisterFlight, RegisterFlightValidator
from src.core.units_of_work import RegisterFlightUoW

router = APIRouter(prefix="/api/flights", tags=["Bookings"])

def get_flight_registrar() -> RegisterFlight:
    db_manager = DBManager()
    register_flight_validator = RegisterFlightValidator(FlightValidator(), AirplaneValidator(), RouteValidator())

    return RegisterFlight(RegisterFlightUoW(db_manager), register_flight_validator)

@router.post("/", response_model=FlightResponse)
def register_flight(flight_request: FlightRequest, flight_registrar: RegisterFlight = Depends(get_flight_registrar)):
    flight_response: FlightResponse = flight_registrar.execute(flight_request)

    return flight_response