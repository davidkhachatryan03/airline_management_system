from datetime import datetime

from src.common.types import AirplaneId, FlightHourCostUsd, RangeKm
from src.entities import Airplane


class FakeAirplaneRepository:

    def __init__(self) -> None:
        self.airplanes: list[Airplane] = []

    def insert_airplanes(self, airplanes: list[Airplane]) -> None:
        self.airplanes.extend(airplanes)

    def retrieve_airplanes_by_id(
        self, airplane_ids: list[AirplaneId]
    ) -> list[AirplaneId]:
        for airplane_stored in self.airplanes:
            if airplane_stored.id == airplane_ids[0]:
                return [airplane_stored.id]

        return []

    def retrieve_available_airplanes_id(
        self,
        range_km: RangeKm,
        scheduled_departure_datetime: datetime,
        scheduled_arrival_datetime: datetime,
    ) -> list[AirplaneId]:
        airplane_available_ids: list[AirplaneId] = []

        for airplane_stored in self.airplanes:
            if airplane_stored.range_km >= range_km:
                airplane_available_ids.append(airplane_stored.id)

        return airplane_available_ids

    def retrieve_flight_hour_cost_usd_by_id(
        self, airplane_ids: list[AirplaneId]
    ) -> list[FlightHourCostUsd]:
        for airplane in self.airplanes:
            if airplane.id == airplane_ids[0]:
                return [airplane.flight_hour_cost_usd]

        return []
