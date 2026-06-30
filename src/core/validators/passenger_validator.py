from uuid import UUID

from src.common.exceptions import BlacklistedPassenger, InvalidPassenger
from src.entities import Passenger

class PassengerValidator:

    def check_blacklisted(self, passengers: list[Passenger]) -> None:
        for passenger in passengers:
            if passenger.is_blacklisted:
                raise BlacklistedPassenger
            
    def check_existence(self, passengers_requested: list[UUID], passengers_retrieved: list[Passenger]) -> None:
        passengers_requested_set = set(passengers_requested)
        for passenger in passengers_retrieved:
            if passenger.id not in passengers_requested_set:
                raise InvalidPassenger