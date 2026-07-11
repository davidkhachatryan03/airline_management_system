from src.common.types import PassengerId, IsBlacklisted

class PassengerValidator:
            
    def check_existence(self, passengers_requested_id: list[PassengerId], passengers_retrieved_id: list[PassengerId]) -> bool:
        missing_ids = set(passengers_requested_id) - set(passengers_retrieved_id)
        
        if missing_ids:
            return False
            
        return True

    def check_blacklisted(self, passengers_statuses: list[IsBlacklisted]) -> bool:
        for status in passengers_statuses:
            if status is True:
                return True
            
        return False