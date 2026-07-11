from decimal import Decimal

from src.api.schemas import FlightRequest, FlightResponse
from src.common.exceptions import DuplicatedFlight, InexistentAirplane, InexistentRoute, MultipleExceptionsError, UnavailableAirplane
from src.common.types import AirplaneId, DistanceKm, FlightIdentityKey, RouteId
from src.core.units_of_work import RegisterFlightUoW
from src.core.validators import AirplaneValidator, FlightValidator, RouteValidator
from src.entities import Flight, Route

class RegisterFlightValidator:
    
    def __init__(self, flight_validator: FlightValidator, airplane_validator: AirplaneValidator, route_validator: RouteValidator) -> None:
        self.flight_validator = flight_validator
        self.airplane_validator = airplane_validator
        self.route_validator = route_validator

    def validate_data_logic(self, 
                            flights_requested: list[FlightIdentityKey], 
                            flights_retrieved: list[FlightIdentityKey], 
                            airplanes_id_retrieved: list[AirplaneId], 
                            routes_id_retrieved: list[RouteId], 
                            airplane_id: AirplaneId, 
                            route_id: RouteId) -> None:

        if self.flight_validator.check_existente_by_identity_key(flights_requested, flights_retrieved):
            raise DuplicatedFlight

        if not self.airplane_validator.check_existence([airplane_id], airplanes_id_retrieved):
            raise InexistentAirplane
        
        if not self.route_validator.check_existence([route_id], routes_id_retrieved):
            raise InexistentRoute
    
    def validate_business_logic(self, airplane_id: AirplaneId, available_airplanes_id: list[AirplaneId]) -> None:
        exceptions: list[Exception] = []

        if not self.airplane_validator.check_availability(airplane_id, available_airplanes_id):
            exceptions.append(UnavailableAirplane())
        
        if exceptions:
            raise MultipleExceptionsError(exceptions)

class RegisterFlight:

    def __init__(self, uow: RegisterFlightUoW, register_flight_validator: RegisterFlightValidator) -> None:
        self.uow = uow
        self.register_flight_validator = register_flight_validator

    def execute(self, flight_request: FlightRequest) -> FlightResponse:
        with self.uow as uow:
            flights_requested_identity_keys: list[FlightIdentityKey] = [flight_request.identity_key]
            routes_requested_id: list[RouteId] = [flight_request.route_id]
            
            flights_retrieved: list[Flight] = uow.flight_repository.retrieve_flights_by_identity_key(flights_requested_identity_keys)
            flights_retrieved_identity_keys: list[FlightIdentityKey] = [flight.identity_key for flight in flights_retrieved]

            airplanes_retrieved_id: list[AirplaneId] = uow.airplane_repository.retrieve_airplanes_by_id(flight_request.airplane_id)

            routes_retrieved: list[Route] = uow.route_repository.retrieve_routes_by_id(routes_requested_id)
            routes_retrieved_id: list[RouteId] = [route.id for route in routes_retrieved]
            
            self.register_flight_validator.validate_data_logic(flights_requested_identity_keys, 
                                                            flights_retrieved_identity_keys, 
                                                            airplanes_retrieved_id, 
                                                            routes_retrieved_id, 
                                                            flight_request.airplane_id, 
                                                            flight_request.route_id)

            available_airplanes_id: list[AirplaneId] = uow.airplane_repository.retrieve_available_airplanes_id(flight_request.scheduled_departure_datetime, flight_request.scheduled_arrival_datetime)

            self.register_flight_validator.validate_business_logic(flight_request.airplane_id, available_airplanes_id)

            flight_hour_cost_usd: Decimal = uow.airplane_repository.retrieve_flight_hour_cost_usd_by_id(flight_request.airplane_id)[0]
            duration_min: DistanceKm = uow.route_repository.retrieve_distance_km_by_id(flight_request.route_id)[0]
            
            flight_created: Flight = Flight.new_flight(
                scheduled_departure_datetime=flight_request.scheduled_departure_datetime,
                scheduled_arrival_datetime=flight_request.scheduled_arrival_datetime,
                operating_cost_usd=Flight._calculate_operating_cost_usd(flight_hour_cost_usd, duration_min),
                route_id=flight_request.route_id,
                airplane_id=flight_request.airplane_id
            )

            uow.flight_repository.insert_flights([flight_created])

            return FlightResponse(id=flight_created.id)     