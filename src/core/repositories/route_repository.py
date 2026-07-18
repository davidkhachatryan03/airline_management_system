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

    def retrieve_routes_by_id(self, routes_id: list[RouteId]) -> list[Route]:
        if not routes_id:
            return []

        placeholders = ",".join(["%s" * len(routes_id)])

        query = "SELECT id, flight_number, origin, destination, distance_km, duration_min FROM routes WHERE id IN ({})".format(
            placeholders
        )

        results: list[RouteRow] = self.db_manager.retrieve_single_column(
            query, routes_id
        )

        if results:
            return [Route(*result) for result in results]

        return []

    def retrieve_distance_km_by_id(self, route_id: RouteId) -> list[DistanceKm]:
        query = "SELECT distance_km FROM routes WHERE id = %s"

        results: list[RouteId] = self.db_manager.retrieve_single_column(
            query, (route_id,)
        )

        if results:
            return results

        return []

    def retrieve_duration_min_by_id(self, route_id: RouteId) -> list[DurationMin]:
        query = "SELECT duration_min FROM routes WHERE id = %s"

        results: list[RouteId] = self.db_manager.retrieve_single_column(
            query, (route_id,)
        )

        if results:
            return results

        return []
