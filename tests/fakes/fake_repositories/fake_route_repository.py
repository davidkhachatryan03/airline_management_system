from src.common.types import DistanceKm, DurationMin, RouteId
from src.entities import Route
from tests.fakes.fake_repositories.fake_base_repository import \
    FakeBaseRepository


class FakeRouteRepository(FakeBaseRepository[Route]):

    def __init__(self) -> None:
        super().__init__()

    def retrieve_distances_km_by_ids(
        self, route_ids: list[RouteId]
    ) -> list[DistanceKm]:
        return [self.storage[route_id].distance_km for route_id in route_ids]

    def retrieve_durations_min_by_ids(
        self, route_ids: list[RouteId]
    ) -> list[DurationMin]:
        return [self.storage[route_id].duration_min for route_id in route_ids]
