from src.core.validators import PassengerValidator
from src.entities import Passenger, Document
from src.api.schemas import PassengerRequest
import uuid6

class PassengerManager:

    def __init__(self, passenger_validator: PassengerValidator) -> None:
        self.passenger_validator = passenger_validator

    def generate_passenger(self, passenger: PassengerRequest) -> Passenger:
        return Passenger(
            id=uuid6.uuid7(),
            national_identity_number=passenger.national_identity_number,
            issue_country=passenger.issue_country,
            full_name=passenger.full_name,
            birth_date=passenger.birth_date,
            email=passenger.email,
            phone_number=passenger.phone_number,
            is_blacklisted=False,
            is_vip=False
    )