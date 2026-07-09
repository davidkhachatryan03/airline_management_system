from src.common.types import PassengerId, IsBlacklisted
from src.entities import Passenger

class PassengerValidator:
            
    def check_existence(self, passengers_requested: list[PassengerId], passengers_retrieved: list[Passenger]) -> bool:
        requested_ids = set(passengers_requested)
        retrieved_ids = {passenger.id for passenger in passengers_retrieved}
        
        missing_ids = requested_ids - retrieved_ids
        
        if missing_ids:
            return False
            
        return True

    def check_blacklisted(self, passengers_statuses: list[IsBlacklisted]) -> bool:
        for status in passengers_statuses:
            if status is True:
                return True
            
        return False