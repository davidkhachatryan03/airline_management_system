from datetime import datetime

from src.api.schemas import FlightRequest, FlightResponse
from src.entities import Airplane, Flight, Route
from src.core.units_of_work import RegisterFlightUoW
from src.core.validators import FlightValidator

class RegisterFlight:

    def __init__(self, uow: RegisterFlightUoW, flight_validator: FlightValidator) -> None:
        self.uow = uow
        self.flight_validator = flight_validator

    def execute(self, flight_request: FlightRequest) -> FlightResponse:
        with self.uow as uow:
            flight_request_identity_key: tuple[datetime, int] = (flight_request.scheduled_departure_datetime, flight_request.route_id)
            flight_retrieved: list[Flight] = uow.flight_repository.retrieve_flights_by_identity_key(flight_request_identity_key)

            if flight_retrieved:
                self.flight_validator.check_flight_not_existence(flight_retrieved[0])

            