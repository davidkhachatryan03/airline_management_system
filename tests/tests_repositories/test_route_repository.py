from factory.declarations import Iterator

from src.common.types import DistanceKm, DurationMin
from src.core.repositories import RouteRepository
from src.entities import Route
from tests.factories import RouteFactory


def test_retrieve_distances_km_by_ids(route_repository: RouteRepository) -> None:
    route_repository.delete()

    distances_km_expected: list[DistanceKm] = [1000, 2000, 3000, 4000]
    routes: list[Route] = RouteFactory.build_batch(
        4, distance_km=Iterator(distances_km_expected)
    )

    route_repository.insert(routes)

    distances_km: list[DistanceKm] = route_repository.retrieve_distances_km_by_ids(
        [route.id for route in routes]
    )

    assert set(distances_km) == set(distances_km_expected)


def test_retrieve_durations_min_by_ids(route_repository: RouteRepository) -> None:
    route_repository.delete()

    durations_min_expected: list[DurationMin] = [120, 60, 280, 240]
    routes: list[Route] = RouteFactory.build_batch(
        4, duration_min=Iterator(durations_min_expected)
    )

    route_repository.insert(routes)

    durations_min: list[DurationMin] = route_repository.retrieve_durations_min_by_ids(
        [route.id for route in routes]
    )

    assert set(durations_min_expected) == set(durations_min)
