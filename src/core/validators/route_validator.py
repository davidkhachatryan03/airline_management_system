from src.common.types import RouteId

class RouteValidator:

    def check_existence(self, routes_requested_id: list[RouteId], routes_retrieved_id: list[RouteId]) -> bool:
        missing_ids = set(routes_requested_id) - set(routes_retrieved_id)
        
        if missing_ids:
            return False
            
        return True
