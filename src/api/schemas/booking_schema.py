from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from src.api.schemas import PassengerRequest

class BookingRequest(BaseModel):
    flights_id: list[UUID] = Field(min_length=1)
    passengers: list[PassengerRequest] = Field(min_length=1)

    @field_validator("flights_id")
    @classmethod
    def validate_flights_id(cls, value: list[UUID]):
        if len(value) != len(set(value)):
            raise ValueError("The flights must be unique.")
        
        return value
        
class BookingResponse(BaseModel):
    booking_reference: str
    tickets: list[str]
    booking_datetime: datetime
    paid_amount_usd: Decimal
    current_status_id: int