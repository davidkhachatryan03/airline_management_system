from src.common.types import DistanceKm, DurationMin, RouteId
from src.entities import Route


class FakeRouteRepository:

    def __init__(self) -> None:
        self.routes: list[Route] = []

    def insert(self, routes: list[Route]) -> None:
        self.routes.extend(routes)

    def retrieve_by_ids(self, route_ids: list[RouteId]) -> list[Route]:
        routes_retrieved: list[Route] = []

        routes_stored_ids: dict[RouteId, Route] = {
            route.id: route for route in self.routes
        }
        for route_id in route_ids:
            if route_id in routes_stored_ids:
                routes_retrieved.append(routes_stored_ids[route_id])

        return routes_retrieved

    def retrieve_distances_km_by_ids(
        self, route_ids: list[RouteId]
    ) -> list[DistanceKm]:
        for route in self.routes:
            if route.id == route_ids[0]:
                return [route.distance_km]

        return []

    def retrieve_durations_min_by_ids(
        self, route_ids: list[RouteId]
    ) -> list[DurationMin]:
        for route in self.routes:
            if route.id == route_ids[0]:
                return [route.duration_min]

        return []
