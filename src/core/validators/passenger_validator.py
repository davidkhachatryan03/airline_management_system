from src.common.types import IsBlacklisted

class PassengerValidator:

    def is_blacklisted(self, passengers_statuses: list[IsBlacklisted]) -> bool:
        if True in passengers_statuses:
            return True
        
        return False