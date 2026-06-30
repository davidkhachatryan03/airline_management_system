from uuid import UUID

from src.common.exceptions import BlacklistedPassenger, InexistentPassenger
from src.entities import Passenger

class PassengerValidator:

    def check_blacklisted(self, passengers: list[Passenger]) -> None:
        for passenger in passengers:
            if passenger.is_blacklisted:
                raise BlacklistedPassenger
            
    def check_existence(self, passengers_requested: list[UUID], passengers_retrieved: list[Passenger]) -> None:
        if not passengers_retrieved:
            raise InexistentPassenger
        
        passengers_requested_set = set(passengers_requested)
        for passenger in passengers_retrieved:
            if passenger.id not in passengers_requested_set:
                raise InexistentPassenger