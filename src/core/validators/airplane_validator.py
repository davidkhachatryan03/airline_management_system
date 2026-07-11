from src.common.types import AirplaneId

class AirplaneValidator:

    def check_existence(self, airplanes_requested_id: list[AirplaneId], airplanes_retrieved_id: list[AirplaneId]) -> bool:
        missing_ids = set(airplanes_requested_id) - set(airplanes_retrieved_id)
        
        if missing_ids:
            return False
            
        return True
    
    def check_availability(self, airplane_id: AirplaneId, available_airplanes: list[AirplaneId]) -> bool:
        return airplane_id in available_airplanes