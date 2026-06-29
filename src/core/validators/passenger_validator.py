from uuid import UUID

from src.common.exceptions import BlacklistedPassenger, InvalidPassenger
from src.entities import Passenger

class PassengerValidator:

    def check_blacklisted(self, passengers: list[Passenger]) -> None:
        for passenger in passengers:
            if passenger.is_blacklisted == True:
                raise BlacklistedPassenger
            
    def check_existence(self, passengers_requested: list[UUID], passengers_retrieved: list[Passenger]) -> None:
        if len(passengers_retrieved) != len(passengers_requested):
            raise InvalidPassenger