from src.common import DBManager
from src.common.types import DistanceKm, DurationMin, RouteId, RouteRow
from src.entities import Route


class RouteRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager

    def retrieve_routes(self, limit: int = 5) -> list[Route]:
        query = "SELECT id, flight_number, origin, destination, distance_km, duration_min FROM routes ORDER BY id DESC LIMIT %s"

        results: list[RouteRow] = self.db_manager.retrieve_many_columns(query, (limit,))

        if results:
            return [Route(*result) for result in results]

        return []

    def retrieve_routes_by_ids(self, route_ids: list[RouteId]) -> list[Route]:
        if not route_ids:
            return []

        placeholders = ",".join(["%s" * len(route_ids)])

        query = "SELECT id, flight_number, origin, destination, distance_km, duration_min FROM routes WHERE id IN ({})".format(
            placeholders
        )

        results: list[RouteRow] = self.db_manager.retrieve_many_columns(
            query, route_ids
        )

        if results:
            return [Route(*result) for result in results]

        return []

    def retrieve_distances_km_by_ids(
        self, route_ids: list[RouteId]
    ) -> list[DistanceKm]:
        if not route_ids:
            return []

        placeholders = ",".join(["%s" * len(route_ids)])

        query = "SELECT distance_km FROM routes WHERE id IN ({})".format(placeholders)

        results: list[RouteId] = self.db_manager.retrieve_single_column(
            query, route_ids
        )

        if results:
            return results

        return []

    def retrieve_durations_min_by_ids(
        self, route_ids: list[RouteId]
    ) -> list[DurationMin]:
        if not route_ids:
            return []

        placeholders = ",".join(["%s" * len(route_ids)])

        query = "SELECT duration_min FROM routes WHERE id IN ({})".format(placeholders)

        results: list[RouteId] = self.db_manager.retrieve_single_column(
            query, route_ids
        )

        if results:
            return results

        return []
