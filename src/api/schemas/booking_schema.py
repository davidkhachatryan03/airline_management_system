from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from decimal import Decimal
from datetime import datetime

class BookingRequest(BaseModel):
    flights_id: list[UUID] = Field(min_length=1)
    passengers_id: list[UUID] = Field(min_length=1)
    paid_amount_usd: Decimal = Field(gt=Decimal("0"))

    @field_validator("flights_id")
    @classmethod
    def validate_flights_id(cls, value: list[UUID]):
        if len(value) != len(set(value)):
            raise ValueError("The flights must be unique.")
        
        return value
        
    @field_validator("passengers_id")
    @classmethod
    def validate_passengers_id(cls, value: list[UUID]):
        if len(value) != len(set(value)):
            raise ValueError("The passengers must be unique.")
        
        return value
        
class BookingResponse(BaseModel):
    booking_reference: str
    tickets: list[str]
    booking_datetime: datetime
    paid_amount_usd: Decimal
    current_status_id: int