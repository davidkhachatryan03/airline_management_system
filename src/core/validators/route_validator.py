from src.common.types import RouteId
from src.entities import Route

class RouteValidator:

    def check_existence(self, routes_requested: list[RouteId], routes_retrieved: list[Route]) -> bool:
        requested_ids = set(routes_requested)
        retrieved_ids = {route.id for route in routes_retrieved}
        
        missing_ids = requested_ids - retrieved_ids
        
        if missing_ids:
            return False
            
        return True
