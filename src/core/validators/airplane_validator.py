from src.common.types import AirplaneId
from src.entities import Airplane

class AirplaneValidator:

    def check_existence(self, airplanes_requested: list[AirplaneId], airplanes_retrieved: list[Airplane]) -> bool:
        requested_ids = set(airplanes_requested)
        retrieved_ids = {airplane.id for airplane in airplanes_retrieved}
        
        missing_ids = requested_ids - retrieved_ids
        
        if missing_ids:
            return False
            
        return True