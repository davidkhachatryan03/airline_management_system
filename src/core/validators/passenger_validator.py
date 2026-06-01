from src.common.exceptions import BlacklistedPassenger
from src.entities import Passenger

class PassengerValidator:

    def check_blacklisted(self, passengers: list[Passenger]) -> None:
        for passenger in passengers:
            if passenger.is_blacklisted == True:
                raise BlacklistedPassenger