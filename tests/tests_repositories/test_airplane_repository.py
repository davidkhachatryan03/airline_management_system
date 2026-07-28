from datetime import datetime

from src.common.types import AirplaneId, FlightHourCostUsd, RangeKm
from src.core.repositories import AirplaneRepository
from src.entities import Airplane


def test_airplane_repository_retrieve_ranges_km_by_ids(
    airplane_repository: AirplaneRepository, airplanes: list[Airplane]
) -> None:
    airplane_repository.insert(airplanes)

    airplane_ids: list[AirplaneId] = [airplane.id for airplane in airplanes]
    ranges_km: list[RangeKm] = [airplane.range_km for airplane in airplanes]

    ranges_km_retrieved: list[RangeKm] = airplane_repository.retrieve_ranges_km_by_ids(
        airplane_ids
    )

    assert set(ranges_km) == set(ranges_km_retrieved)


def test_ariplane_repository_retrieve_flight_hour_costs_by_ids(
    airplane_repository: AirplaneRepository, airplanes: list[Airplane]
) -> None:
    airplane_repository.insert(airplanes)

    airplane_ids: list[AirplaneId] = [airplane.id for airplane in airplanes]
    flight_hour_costs_usd: list[FlightHourCostUsd] = [
        airplane.flight_hour_cost_usd for airplane in airplanes
    ]

    flight_hour_costs_usd_retrieved: list[FlightHourCostUsd] = (
        airplane_repository.retrieve_flight_hour_costs_usd_by_ids(airplane_ids)
    )

    assert set(flight_hour_costs_usd) == set(flight_hour_costs_usd_retrieved)


def test_retrieve_available_airplanes_ids(
    airplane_repository: AirplaneRepository, airplanes: list[Airplane]
) -> None:
    airplane_repository.insert(airplanes)

    airplane_ids: list[AirplaneId] = [airplane.id for airplane in airplanes]

    available_airplane_ids_retrieved: list[AirplaneId] = (
        airplane_repository.retrieve_available_airplanes_ids(
            100, datetime(2026, 1, 1), datetime(2026, 1, 2)
        )
    )

    assert set(airplane_ids) == set(available_airplane_ids_retrieved)


def test_retrieve_available_airplanes_ids_empty(
    airplane_repository: AirplaneRepository, airplanes: list[Airplane]
) -> None:
    airplane_repository.insert(airplanes)

    available_airplanes_retrieved: list[AirplaneId] = (
        airplane_repository.retrieve_available_airplanes_ids(
            99999999999, datetime(2026, 1, 1), datetime(2026, 1, 2)
        )
    )

    assert available_airplanes_retrieved == []
