from decimal import Decimal, ROUND_HALF_UP

from src.api.schemas import FlightRequest, FlightResponse
from src.entities import Flight
from src.core.units_of_work import RegisterFlightUoW
from src.core.validators import FlightValidator
from src.common.types import DurationMin

class RegisterFlight:

    def __init__(self, uow: RegisterFlightUoW, flight_validator: FlightValidator) -> None:
        self.uow = uow
        self.flight_validator = flight_validator

    def execute(self, flight_request: FlightRequest) -> FlightResponse:
        with self.uow as uow:
            flight_retrieved: list[Flight] = uow.flight_repository.retrieve_flights_by_identity_key([flight_request.identity_key])

            if flight_retrieved:
                self.flight_validator.check_flight_not_existence(flight_retrieved[0])
            
            flight_created = Flight.new_flight(
                scheduled_departure_datetime=flight_request.scheduled_departure_datetime,
                scheduled_arrival_datetime=flight_request.scheduled_arrival_datetime,
                operating_cost_usd=
            )

            uow.flight_repository.insert_flights()

    def _calculate_operating_cost_usd(self, flight_hour_cost_usd: Decimal, duration_min: DurationMin) -> Decimal:
        return (flight_hour_cost_usd * duration_min).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)