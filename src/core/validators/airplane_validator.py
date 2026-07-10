from src.common.types import AirplaneId
from src.entities import Airplane

class AirplaneValidator:

    def check_existence(self, airplanes_requested: list[AirplaneId], airplanes_retrieved: list[AirplaneId]) -> bool:
        requested_ids = set(airplanes_requested)
        retrieved_ids = {airplane for airplane in airplanes_retrieved}
        
        missing_ids = requested_ids - retrieved_ids
        
        if missing_ids:
            return False
            
        return True
    
    def check_availability(self, airplane_id: AirplaneId, available_airplanes: list[AirplaneId]) -> bool:
        return airplane_id in available_airplanes