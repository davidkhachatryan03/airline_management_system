from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from src.api.schemas.passenger_schema import PassengerRequest
from src.common.types import (BoardingDatetime, BookingReference, FlightId,
                            PaidAmountUsd, TicketNumber)


class BookingRequest(BaseModel):
    flights_id: list[FlightId] = Field(min_length=1)
    passengers: list[PassengerRequest] = Field(min_length=1)

    @field_validator("flights_id")
    @classmethod
    def validate_flights_id(cls, value: list[FlightId]):
        if len(value) != len(set(value)):
            raise ValueError("The flights must be unique.")

        return value


class BookingResponse(BaseModel):
    booking_reference: BookingReference
    tickets: list[TicketNumber]
    booking_datetime: BoardingDatetime = Field(default_factory=datetime.now)
    paid_amount_usd: PaidAmountUsd = Field(gt=0, decimal_places=2, max_digits=8)
