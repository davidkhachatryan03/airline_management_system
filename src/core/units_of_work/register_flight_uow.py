from src.common import DBManager
from src.core.repositories import (AirplaneRepository, FlightRepository,
                                   RouteRepository)


class RegisterFlightUoW:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager
        self.airplane_repository = AirplaneRepository(db_manager)
        self.flight_repository = FlightRepository(db_manager)
        self.route_repository = RouteRepository(db_manager)

    def __enter__(self):
        self.db_manager.__enter__()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        return self.db_manager.__exit__(exception_type, exception_value, traceback)
