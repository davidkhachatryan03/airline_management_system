from src.common.exceptions import BlacklistedPassenger, InvalidPassenger
from src.entities import Passenger
from uuid import UUID

class PassengerValidator:

    def check_blacklisted(self, passengers: list[Passenger]) -> None:
        for passenger in passengers:
            if passenger.is_blacklisted == True:
                raise BlacklistedPassenger
            
    def check_existence(self, passengers_requested: list[UUID], passengers_retrieved: list[Passenger]) -> None:
        for passenger in passengers_retrieved:
            if passenger.id not in passengers_requested:
                raise InvalidPassenger