from src.common.types import DistanceKm, DurationMin, RouteId
from src.entities import Route


class FakeRouteRepository:

    def __init__(self) -> None:
        self.routes: list[Route] = []

    def insert_routes(self, routes: list[Route]) -> None:
        self.routes.extend(routes)

    def retrieve_routes_by_id(self, routes: list[RouteId]) -> list[Route]:
        routes_retrieved: list[Route] = []
        dict_routes_stored_ids: dict[RouteId, Route] = {
            route.id: route for route in self.routes
        }

        for route in routes:
            if route in dict_routes_stored_ids:
                routes_retrieved.append(dict_routes_stored_ids[route])

        return routes_retrieved

    def retrieve_distance_km_by_id(self, routes_id: list[RouteId]) -> list[DistanceKm]:
        for route in self.routes:
            if route.id == routes_id[0]:
                return [route.distance_km]

        return []

    def retrieve_duration_min_by_id(self, routes_id: list[RouteId]) -> list[DurationMin]:
        for route in self.routes:
            if route.id == routes_id[0]:
                return [route.duration_min]

        return []