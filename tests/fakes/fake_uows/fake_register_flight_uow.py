from tests.fakes.fake_db_manager import FakeDBManager
from tests.fakes.fake_repositories import (FakeAirplaneRepository,
                                           FakeFlightRepository,
                                           FakeRouteRepository)


class FakeRegisterFlightUoW:

    def __init__(self, db_manager: FakeDBManager) -> None:
        self.db_manager = db_manager
        self.airplane_repository = FakeAirplaneRepository()
        self.flight_repository = FakeFlightRepository()
        self.route_repository = FakeRouteRepository()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        pass