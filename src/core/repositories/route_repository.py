from src.common import DBManager
from src.common.types import DistanceKm, DurationMin, RouteId
from src.core.repositories.base_repository import BaseRepository
from src.entities import Route


class RouteRepository(BaseRepository[Route]):

    def __init__(self, db_manager: DBManager) -> None:
        super().__init__(
            db_manager=db_manager,
            table_name="routes",
            columns=(
                "id",
                "flight_number",
                "origin",
                "destination",
                "distance_km",
                "duration_min",
            ),
            entity=Route,
        )

    def retrieve_distances_km_by_ids(
        self, route_ids: list[RouteId]
    ) -> list[DistanceKm]:
        if not route_ids:
            return []

        placeholders = ",".join(["%s"] * len(route_ids))

        query = "SELECT distance_km FROM routes WHERE id IN ({})".format(placeholders)

        results: list[RouteId] = self.db_manager.execute_read_single_column(
            query, route_ids
        )

        return results

    def retrieve_durations_min_by_ids(
        self, route_ids: list[RouteId]
    ) -> list[DurationMin]:
        if not route_ids:
            return []

        placeholders = ",".join(["%s"] * len(route_ids))

        query = "SELECT duration_min FROM routes WHERE id IN ({})".format(placeholders)

        results: list[RouteId] = self.db_manager.execute_read_single_column(
            query, route_ids
        )

        return results
