from pydantic import BaseModel, Field, field_validator
from decimal import Decimal
from datetime import datetime

class BookingRequest(BaseModel):
    flights_id: list[int] = Field(min_length=1)
    passengers_id: list[int] = Field(min_length=1)
    paid_amount_usd: Decimal = Field(gt=Decimal("0"))

    @field_validator("flights_id")
    @classmethod
    def validate_flights_id(cls, value: str):
        if len(value) == len(set(value)):
            raise ValueError("The flights must be unique.")
        
    @field_validator("passengers_id")
    @classmethod
    def validate_passengers_id(cls, value: str):
        if len(value) == len(set(value)):
            raise ValueError("The passengers must be unique.")
        
class BookingResponse(BaseModel):
    id: int
    booking_reference: str
    tickets: list[str]
    booking_datetime: datetime
    paid_amount_usd: Decimal
    current_status_id: int