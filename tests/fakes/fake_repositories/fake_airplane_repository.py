from datetime import datetime

from src.common.types import AirplaneId, FlightHourCostUsd, RangeKm
from src.entities import Airplane
from tests.fakes.fake_repositories.fake_base_repository import FakeBaseRepository


class FakeAirplaneRepository(FakeBaseRepository[Airplane]):

    def __init__(self) -> None:
        super().__init__()

    def retrieve_available_airplanes_ids(
        self,
        range_km: RangeKm,
        scheduled_departure_datetime: datetime,
        scheduled_arrival_datetime: datetime,
    ) -> list[AirplaneId]:
        airplane_available_ids: list[AirplaneId] = []

        for airplane_stored in list(self.storage.values()):
            if airplane_stored.range_km >= range_km:
                airplane_available_ids.append(airplane_stored.id)

        return airplane_available_ids

    def retrieve_flight_hour_costs_usd_by_ids(
        self, airplane_ids: list[AirplaneId]
    ) -> list[FlightHourCostUsd]:
        flight_hour_cost_ids: list[FlightHourCostUsd] = []

        for airplane in list(self.storage.values()):
            if airplane.id == airplane_ids[0]:
                flight_hour_cost_ids.append(airplane.flight_hour_cost_usd)

        return flight_hour_cost_ids
