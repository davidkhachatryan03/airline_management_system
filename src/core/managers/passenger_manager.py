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
            full_name=passenger.full_name,
            birth_date=passenger.birth_date,
            email=passenger.email,
            phone_number=passenger.phone_number,
            is_blacklisted=False,
            is_vip=False
    )

    def generate_document(self, passenger: PassengerRequest, passenger_created: Passenger) -> Document:
        return Document(
            id=uuid6.uuid7(),
            document_number=passenger.document_number,
            valid_from=passenger.valid_from,
            valid_until=passenger.valid_until,
            issue_country=passenger.issue_country,
            passenger_id=passenger_created.id,
            document_type_id=passenger.document_type_id
        )