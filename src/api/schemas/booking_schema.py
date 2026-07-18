from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from src.api.schemas.passenger_schema import PassengerRequest


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
    booking_datetime: datetime = Field(default_factory=datetime.now)
    paid_amount_usd: Decimal = Field(gt=0, decimal_places=2, max_digits=8)
