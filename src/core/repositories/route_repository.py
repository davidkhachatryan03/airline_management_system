from src.common import DBManager
from src.entities import Route

class RouteRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager

    def retrieve_routes(self, limit: int = 5) -> list[Route]:
        query = "SELECT * FROM routes ORDER BY id DESC LIMIT %s"

        results: list[tuple] = self.db_manager.retrieve(query, (limit,))
        
        if results:
            return [Route(*result) for result in results]
        
        return []