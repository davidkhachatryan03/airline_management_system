from decimal import Decimal

from src.api.schemas import FlightRequest, FlightResponse
from src.common.exceptions import (
    DuplicatedFlight,
    InexistentAirplane,
    InexistentRoute,
    InvalidData,
    MultipleExceptionsError,
    UnavailableAirplane,
)
from src.common.types import AirplaneId, DurationMin, FlightIdentityKey, RouteId
from src.core.units_of_work import RegisterFlightUoW
from src.core.validators import BaseValidator, FlightValidator
from src.entities import Flight, Route


class RegisterFlightValidator:

    def __init__(
        self, base_validator: BaseValidator, flight_validator: FlightValidator
    ) -> None:
        self.base_validator = base_validator
        self.flight_validator = flight_validator

    def validate_data_logic(
        self,
        airplanes_id_retrieved: list[AirplaneId],
        routes_id_retrieved: list[RouteId],
        airplane_id: AirplaneId,
        route_id: RouteId,
    ) -> None:
        exceptions: list[InvalidData] = []

        airplanes_missing_ids: set[AirplaneId] = self.base_validator.check_existence(
            [airplane_id], airplanes_id_retrieved
        )
        if airplanes_missing_ids:
            for airplane_id in airplanes_missing_ids:
                exceptions.append(InexistentAirplane(airplane_id))

        routes_missing_ids: set[RouteId] = self.base_validator.check_existence(
            [route_id], routes_id_retrieved
        )
        if routes_missing_ids:
            for route_id in routes_missing_ids:
                exceptions.append(InexistentRoute(route_id))

        if exceptions:
            raise MultipleExceptionsError(exceptions)

    def validate_business_logic(
        self,
        flights_requested_identity_keys: list[FlightIdentityKey],
        flights_retrieved_identity_keys: list[FlightIdentityKey],
        airplane_id: AirplaneId,
        available_airplanes_id: list[AirplaneId],
    ) -> None:
        exceptions: list[InvalidData] = []

        flight_requested_identity_key: set[FlightIdentityKey] = (
            self.base_validator.check_existence(
                flights_requested_identity_keys, flights_retrieved_identity_keys
            )
        )
        available_airplane_id: set[AirplaneId] = self.base_validator.check_existence(
            [airplane_id], available_airplanes_id
        )

        if not flight_requested_identity_key:
            exceptions.append(DuplicatedFlight(flights_requested_identity_keys[0]))

        if available_airplane_id:
            exceptions.append(UnavailableAirplane(available_airplane_id.pop()))

        if exceptions:
            raise MultipleExceptionsError(exceptions)


class RegisterFlight:

    def __init__(
        self, uow: RegisterFlightUoW, register_flight_validator: RegisterFlightValidator
    ) -> None:
        self.uow = uow
        self.register_flight_validator = register_flight_validator

    def execute(self, flight_request: FlightRequest) -> FlightResponse:
        with self.uow as uow:
            flights_requested_identity_keys: list[FlightIdentityKey] = [
                flight_request.identity_key
            ]
            routes_requested_id: list[RouteId] = [flight_request.route_id]

            flights_retrieved: list[Flight] = (
                uow.flight_repository.retrieve_flights_by_identity_key(
                    flights_requested_identity_keys
                )
            )
            flights_retrieved_identity_keys: list[FlightIdentityKey] = [
                flight.identity_key for flight in flights_retrieved
            ]

            airplanes_retrieved_id: list[AirplaneId] = (
                uow.airplane_repository.retrieve_airplanes_by_id(
                    flight_request.airplane_id
                )
            )

            routes_retrieved: list[Route] = uow.route_repository.retrieve_routes_by_id(
                routes_requested_id
            )
            routes_retrieved_id: list[RouteId] = [
                route.id for route in routes_retrieved
            ]

            self.register_flight_validator.validate_data_logic(
                airplanes_retrieved_id,
                routes_retrieved_id,
                flight_request.airplane_id,
                flight_request.route_id,
            )

            available_airplanes_id: list[AirplaneId] = (
                uow.airplane_repository.retrieve_available_airplanes_id(
                    routes_retrieved[0].distance_km,
                    flight_request.scheduled_departure_datetime,
                    flight_request.scheduled_arrival_datetime,
                )
            )

            self.register_flight_validator.validate_business_logic(
                flights_requested_identity_keys,
                flights_retrieved_identity_keys,
                flight_request.airplane_id,
                available_airplanes_id,
            )

            flight_hour_cost_usd: Decimal = (
                uow.airplane_repository.retrieve_flight_hour_cost_usd_by_id(
                    flight_request.airplane_id
                )[0]
            )
            duration_min: DurationMin = (
                uow.route_repository.retrieve_duration_min_by_id(
                    flight_request.route_id
                )[0]
            )

            flight_created = Flight.new_flight(
                scheduled_departure_datetime=flight_request.scheduled_departure_datetime,
                scheduled_arrival_datetime=flight_request.scheduled_arrival_datetime,
                operating_cost_usd=Flight._calculate_operating_cost_usd(
                    flight_hour_cost_usd, duration_min
                ),
                route_id=flight_request.route_id,
                airplane_id=flight_request.airplane_id,
            )

            uow.flight_repository.insert_flights([flight_created])

            return FlightResponse(id=flight_created.id)
