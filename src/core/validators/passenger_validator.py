from src.common.types import PassengerId
from src.entities import Passenger


class PassengerValidator:

    def is_blacklisted(self, passengers: list[Passenger]) -> list[PassengerId]:
        passengers_blacklisted: list[PassengerId] = []

        for passenger in passengers:
            if passenger.is_blacklisted:
                passengers_blacklisted.append(passenger.id)
        
        return passengers_blacklisted