from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
import uuid6, random
from src.common.data_generator.data_generator import DataGenerator
from src.entities import Flight, RouteRetrieved, AirplaneRetrieved

class FlightsGenerator(DataGenerator):

    def __init__(self) -> None:
        super().__init__()
        self.routes = self.retrieve_routes()
        self.airplanes = self.retrieve_airplanes()

    def generate_flights(self, n=50) -> list[Flight]:
        flights: list[Flight] = []

        route: RouteRetrieved = random.choice(self.routes)
        airplane: AirplaneRetrieved = random.choice(self.airplanes)

        scheduled_departure_datetime: date = self.fake.date_time_between(start_date="+30d", end_date="+180d")
        scheduled_arrival_datetime: date = scheduled_departure_datetime + timedelta(minutes=route.duration_min)

        operating_cost_usd: Decimal = self.calculate_operating_cost_usd(airplane.flight_hour_cost_usd, route.duration_min)
        base_price_usd: Decimal = (operating_cost_usd * Decimal("1.3")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        for _ in range(n):
            flight = Flight(
                id=uuid6.uuid7(),
                scheduled_departure_datetime=scheduled_departure_datetime,
                scheduled_arrival_datetime=scheduled_arrival_datetime,
                actual_departure_datetime=None,
                actual_arrival_datetime=None,
                operating_cost_usd=operating_cost_usd,
                base_price_usd=base_price_usd,
                current_status_id=1,
                route_id=route.id,
                airplane_id=airplane.id
            )

            if self.validate_flight(flight):
                flights.append(flight)

        return flights

    def retrieve_routes(self) -> list[RouteRetrieved]:
        with self.db_manager:
            results: list[tuple] = self.db_manager.retrieve("SELECT * FROM routes")

        routes: list[RouteRetrieved] = [RouteRetrieved(*result) for result in results]

        return routes
    
    def retrieve_airplanes(self) -> list[AirplaneRetrieved]:
        with self.db_manager:
            results: list[tuple] = self.db_manager.retrieve("SELECT * FROM airplanes")

        airplanes: list[AirplaneRetrieved] = [AirplaneRetrieved(*result) for result in results]

        return airplanes
    
    def calculate_operating_cost_usd(self, flight_hour_cost_usd: Decimal, duration_min: int) -> Decimal:
        return (flight_hour_cost_usd * duration_min / 60).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)