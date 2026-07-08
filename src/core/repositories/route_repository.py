from src.common import DBManager
from src.common.types import RouteRow
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